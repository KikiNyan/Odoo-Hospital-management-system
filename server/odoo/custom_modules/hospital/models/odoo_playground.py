from odoo import api, fields, models

# Define DEFAULT_ENV_VARIABLE
DEFAULT_ENV_VARIABLE = "Default code value"



class odooplayground(models.Model):
    _name = "odoo.playground"
    _description = "Odoo playground"

    model_id = fields.Many2one('ir.model', string='Model')
    code = fields.Text(string='Code', default=DEFAULT_ENV_VARIABLE)
    result = fields.Text(string='Result')

    def action_execute(self):
        try:
            if self.model_id:
                model = self.env[self.model_id.model]
            else:
                model = self

            self.result = safe_eval(self.code.strip(), {'self': model})

        except Exception as e:
            self.result = str(e)