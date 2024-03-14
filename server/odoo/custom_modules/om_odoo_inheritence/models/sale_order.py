from odoo import api,fields,models

class SaleOrder(models.Model):
  _inherit = "sale.order"

  name = fields.Char(string="Name", required=True)

  confirmed_user_id = fields.Many2one('res.users', string='Confirmed User')