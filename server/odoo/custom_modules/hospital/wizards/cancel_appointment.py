from datetime import date

from odoo import api, fields, models , _
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment', domain=[('state', '=', 'draft'), ('priority', 'in', ('0', '1', False))])
    reason = fields.Text(string='Reason')
    cancel_date = fields.Datetime(string='cancellation Date', default=fields.Datetime.now)


    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['cancel_date'] = date.today()  # Use date.today() to get the current date
        return res

    def action_cancel_appointment(self):
        cancel_days = self.env['ir.config_parameter'].get_param('hospital.cancel_days')
        allowed_date = self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_days))
        if allowed_date < fields.Date.today():
            raise ValidationError(_("Sorry, cancellation is not allowed on the same day"))
        self.appointment_id.state = 'cancel'
        return {
            'type': 'ir.actions.clients',
            'tag': 'reload'
        }

        # reload screen code



        # if self.appointment_id.booking_date == fields.date.today():
        #     raise ValidationError(_("sorry cancellation not allowed on same day"))
        # self.appointment_id.state = 'cancel'
        # return
