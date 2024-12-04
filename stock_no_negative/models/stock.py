from odoo import _, models
from odoo.exceptions import UserError

class StockQuant(models.Model):
    _inherit = "stock.quant"

    def _get_available_quantity(
        self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, strict=False, allow_negative=False
    ):
        # Llamada a super() para obtener la cantidad disponible
        res = super()._get_available_quantity(
            product_id=product_id,
            location_id=location_id,
            lot_id=lot_id,
            package_id=package_id,
            owner_id=owner_id,
            strict=strict,
            allow_negative=allow_negative,
        )

        # Validación para ubicación de origen únicamente
        if location_id and not location_id.allow_negative_stock and res < 0.0:
            if location_id.usage == "production":
                err = _(
                   "El proceso genera stock Negativo. Quedan %(lot_qty)s unidades de %(product_name)s en la ubicación %(location_name)s origen. Por favor, ajusta tus cantidades o corrige tu inventario con un ajuste de inventario."
                ) % {
                    "lot_qty": res,
                    "product_name": product_id.name,
                    "location_name": location_id.name,
                }
                raise UserError(err)

            elif location_id.usage == "internal" :
                err = _(
                    "El proceso genera stock Negativo. Quedan %(lot _qty)s unidades de %(product_name)s en la ubicación %(location_name)s origen. Por favor, ajusta tus cantidades o corrige tu inventario con un ajuste de inventario."
                ) % {
                    "lot_qty": res,
                    "product_name": product_id.name,
                    "location_name": location_id.name,
                }
            elif location_id.usage == "transit" :
                err = _(
                    "El proceso genera stock Negativo. Quedan %(lot_qty)s unidades de %(product_name)s en la ubicación %(location_name)s origen. Por favor, ajusta tus cantidades o corrige tu inventario con un ajuste de inventario."
                ) % {
                    "lot_qty": res,
                    "product_name": product_id.name,
                    "location_name": location_id.name,
                }
                raise UserError(err)

        return res
