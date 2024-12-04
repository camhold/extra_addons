from odoo import models, fields, _, api
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    # Cambiamos mp_flujo_ids a mp_flujo_id, ya que la relación es Many2one
    mp_flujo_id = fields.Many2one(
        'mp.flujo', string="Flujo"
    )
    mp_grupo_flujo_id = fields.Many2one(
        'mp.grupo.flujo', string="Grupo de Flujo"
    )
    
    partner_vat = fields.Char(
        string='VAT',
        related='partner_id.vat',
        readonly=True,
        store=True  # Almacenar para que sea más eficiente en vistas tree
    )

    def action_post(self):
        # Llamada al método original
        res = super(AccountMove, self).action_post()

        for move in self:
            if move.payment_id:
                # Si el pago tiene valores de flujo y grupo de flujo asignados
                if move.payment_id.mp_flujo_id and move.payment_id.mp_grupo_flujo_id:
                    move.sudo().write({
                        'mp_flujo_id': move.payment_id.mp_flujo_id.id,
                        'mp_grupo_flujo_id': move.payment_id.mp_grupo_flujo_id.id
                    })

                    # Asignar estos valores a las líneas del asiento también
                    for line in move.line_ids:
                        line.sudo().write({
                            'mp_flujo_id': move.payment_id.mp_flujo_id.id,
                            'mp_grupo_flujo_id': move.payment_id.mp_grupo_flujo_id.id
                        })
        return res


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # Cambiamos mp_flujo_ids a mp_flujo_id, ya que la relación es Many2one
    mp_flujo_id = fields.Many2one(
        related='move_id.mp_flujo_id', store=True, string="Flujo"
    )
    mp_grupo_flujo_id = fields.Many2one(
        related='move_id.mp_grupo_flujo_id', store=True, string="Grupo de Flujo"
    )

    def action_register_payment(self):
        move_ids = self.mapped('move_id')  # Obtener todos los movimientos relacionados
        if not move_ids:
            raise UserError('No hay movimientos relacionados.')
        res = super(AccountMoveLine, self).action_register_payment()
        if move_ids and move_ids[0].mp_flujo_id and move_ids[0].mp_grupo_flujo_id:
            # Obtener los valores de flujo y grupo de flujo de referencia
            mp_flujo_id = move_ids[0].mp_flujo_id
            mp_grupo_flujo_id = move_ids[0].mp_grupo_flujo_id

            # Verificar si todos los movimientos tienen los mismos valores de flujo y grupo de flujo
            if not all(
                    move.mp_flujo_id == mp_flujo_id and move.mp_grupo_flujo_id == mp_grupo_flujo_id for move in move_ids):
                raise UserError('Existen diferentes valores de flujo o grupo de flujo en los movimientos seleccionados.')

            for move_id in move_ids:
                lines = self.env['account.move.line'].search([
                    ('move_id', '=', move_id.id)
                ])
                if any(line.balance != 0 for line in lines):
                    context = res.get('context')
                    context['default_mp_grupo_flujo_id'] = mp_grupo_flujo_id.id
                    context['mp_flujo_id'] = mp_flujo_id.id
                    res['context'] = context
                # else:
                #     print(f"El move_id {move_id.id} no está parcialmente pagado.")

        return res


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    @api.onchange('mp_grupo_flujo_id')
    def onchange_grupo_flujo(self):
        print('smn')
        mp_flujo_id = self.env['mp.flujo'].search([('id', '=', self._context.get('mp_flujo_id'))])
        if mp_flujo_id:
            self.mp_flujo_id = mp_flujo_id
