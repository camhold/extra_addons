from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def validate_picking(self, picking):
        """
        Validamos las cantidades y productos para el picking IN.
        Se realiza la validación con el picking OUT original o con el backorder relacionado.
        """
        if picking.picking_type_code == 'incoming':
            origin = picking.origin  # Obtener el origen del picking IN
            if origin:
                # Buscar el picking OUT relacionado con el picking IN
                out_pickings = self.env['stock.picking'].search([
                    ('origin', '=', origin),
                    ('picking_type_code', '=', 'outgoing'),
                    ('state', '=', 'done'),  # Solo pickings OUT validados
                ])
                
                if not out_pickings:
                    raise UserError(f"No se encontró un picking OUT validado relacionado con el picking IN {picking.name}.")

                # Validamos las líneas del picking IN con las líneas de los pickings OUT relacionados
                for out_picking in out_pickings:
                    # Si el picking OUT tiene un backorder, validamos solo contra el picking OUT original
                    if out_picking.backorder_id:
                        _logger.info(f"El picking OUT {out_picking.name} (ID: {out_picking.id}) tiene un backorder, se valida con el picking OUT original (ID: {out_picking.id}).")
                        self.validate_backorder_picking(picking, out_picking)  # Validar contra el picking OUT original
                        break  # Salir después de validar el backorder
                    else:
                        # Si no tiene backorder, validamos con el picking OUT normal
                        _logger.info(f"Validando picking OUT {out_picking.name} (ID: {out_picking.id}) con el picking IN {picking.name} (ID: {picking.id}).")
                        self.validate_standard_picking(picking, out_picking)
                        break  # Salir después de la validación de picking OUT normal

            else:
                raise UserError("No se encontró el origen relacionado para el picking.")

        return True

    def validate_standard_picking(self, picking, out_picking):
        """
        Valida el picking estándar (sin backorder).
        Compara las líneas de productos y cantidades entre el picking IN y OUT.
        """
        missing_products = []
        for move in out_picking.move_line_ids:  # Cambiado de move_lines a move_line_ids
            # Comprobamos si el producto de OUT está presente en IN
            in_lines = picking.move_line_ids.filtered(lambda m: m.product_id == move.product_id)  # Cambié de move_lines a move_line_ids
            _logger.info(f"Comparando producto: {move.product_id.display_name} - OUT picking {out_picking.name} (ID: {out_picking.id}), IN picking {picking.name} (ID: {picking.id})")
            
            if len(in_lines) == 0:
                # Si no está presente, agregamos el producto a la lista de productos faltantes
                missing_products.append(f"{move.product_id.display_name} - Cantidad: {move.quantity}")  # Cambié 'product_uom_qty' por 'quantity'
            elif len(in_lines) > 1:
                # Si hay más de una línea de entrada para este producto, sumamos las cantidades
                total_in_quantity = sum(in_line.quantity for in_line in in_lines)
                _logger.info(f"Se encontraron múltiples líneas para el producto {move.product_id.display_name} en el picking IN {picking.name}. Sumando cantidades: {total_in_quantity} unidades.")
                if total_in_quantity != move.quantity:
                    raise UserError(f"Discrepancia en la cantidad total de {move.product_id.display_name}. "
                                    f"El picking OUT tiene {move.quantity} unidades, pero el IN tiene {total_in_quantity} unidades.")
            else:
                # Si hay exactamente una línea de entrada para este producto, comparamos las cantidades
                in_line = in_lines[0]
                _logger.info(f"Comparando cantidad del producto {move.product_id.display_name}: "
                            f"OUT tiene {move.quantity} unidades, IN tiene {in_line.quantity} unidades.")  # Cambié 'product_uom_qty' por 'quantity'
                if move.quantity != in_line.quantity:  # Usamos 'quantity' ya que 'quantity_product_uom' se usa en UOM
                    raise UserError(f"Discrepancia en la cantidad de {move.product_id.display_name}. "
                                    f"El picking OUT tiene {move.quantity} unidades, pero el IN tiene {in_line.quantity} unidades.")
        
        # Si faltan productos, lanzamos un error indicando que se necesita crear una orden parcial
        if missing_products:
            raise UserError(f"Los siguientes productos no fueron registrados en el picking OUT relacionado con el IN {picking.name} (ID: {picking.id}): "
                            f"{', '.join(missing_products)}. "
                            "Se debe crear una orden parcial para estos productos.")

    def validate_backorder_picking(self, picking, out_picking):
        """
        Valida el picking cuando hay un backorder relacionado.
        Compara las líneas de productos y cantidades con el backorder.
        """
        missing_products = []
        for move in out_picking.move_line_ids:  # Cambiado de move_lines a move_line_ids
            # Comprobamos si el producto de BACKORDER está presente en IN
            in_lines = picking.move_line_ids.filtered(lambda m: m.product_id == move.product_id)  # Cambié de move_lines a move_line_ids
            _logger.info(f"Comprobando backorder: {move.product_id.display_name}, cantidad en BACKORDER: {move.quantity}, picking BACKORDER ID: {out_picking.id}")  # Cambié 'product_uom_qty' por 'quantity'
            
            if len(in_lines) == 0:
                # Si no está presente, agregamos el producto a la lista de productos faltantes
                missing_products.append(f"{move.product_id.display_name} - Cantidad: {move.quantity}")  # Cambié 'product_uom_qty' por 'quantity'
            elif len(in_lines) == 1:
                # Si hay exactamente una línea de entrada para este producto, comparamos las cantidades
                in_line = in_lines[0]
                _logger.info(f"Comparando cantidad de backorder para {move.product_id.display_name}: "
                            f"BACKORDER tiene {move.quantity} unidades, IN tiene {in_line.quantity} unidades.")  # Cambié 'product_uom_qty' por 'quantity'
                if move.quantity != in_line.quantity:
                    raise UserError(f"Discrepancia en la cantidad de {move.product_id.display_name}. "
                                    f"El backorder tiene {move.quantity} unidades, pero el IN tiene {in_line.quantity} unidades.")
            else:
                # Si hay más de una línea, se validan las cantidades de todas las líneas
                total_in_quantity = sum(in_line.quantity for in_line in in_lines)
                if total_in_quantity != move.quantity:
                    raise UserError(f"Discrepancia en la cantidad total de {move.product_id.display_name}. "
                                    f"El backorder tiene {move.quantity} unidades, pero el total en el IN es {total_in_quantity} unidades.")

        # Si faltan productos en el backorder, lanzamos un error indicando que se necesita crear una orden parcial
        if missing_products:
            raise UserError(f"Los siguientes productos no fueron registrados en el picking OUT relacionado con el IN {picking.name} (ID: {picking.id}): "
                            f"{', '.join(missing_products)}. "
                            "Se debe crear una orden parcial para estos productos.")

    def button_validate(self):
        """
        Sobrescribimos el botón de validación para incluir la lógica de validación
        antes de realizar la validación final.
        """
        # Solo validamos los pickings de tipo 'incoming' (IN)
        if self.picking_type_code == 'incoming':
            _logger.info(f"Validando picking IN: {self.name} (ID: {self.id})")
            self.validate_picking(self)
        
        # Si el picking es de tipo OUT, dejamos que siga el flujo normal
        if self.picking_type_code == 'outgoing':
            return super(StockPicking, self).button_validate()
        
        # Si el picking es de tipo IN, validamos la lógica antes de proceder
        if self.picking_type_code == 'incoming':
            # Si no se encuentra ningún error en la validación, ejecutamos el proceso de validación de IN
            return super(StockPicking, self).button_validate()
