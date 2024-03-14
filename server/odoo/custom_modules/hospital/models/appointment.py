from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'patient_id'
    _order = 'id desc'
    # ondelete='cascade' delete all foreign key releated with patient id
    name = fields.Char(string='Name', tracking=True)
    progress = fields.Integer(string="Progress", compute='_compute_progress', store=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient", ondelete='restrict')
    appointment_time = fields.Datetime(string='Appointment time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    gender = fields.Selection(related='patient_id.gender', readonly=False)
    reference = fields.Char(string='Reference')
    prescription = fields.Html(string='Prescription')
    doctor_id = fields.Many2one('res.users', string='Doctor', tracking=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority",
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default='draft', string="Status", required=True
    )
    hide_sales_price=fields.Boolean(string='Hide Sale Price')
    duration = fields.Float(string="Duration")

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                rec.progress = 25
            elif rec.state == 'in_consultation':
                rec.progress = 50
            elif rec.state == 'done':
                rec.progress = 100
            else:
                rec.progress = 0

    def action_share_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError(_("Missing phone number of patient"))

        msg = 'HI *%s*, your *appointment* number is: %s. Thank you' % (self.patient_id.name, self.name)
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone, msg)

        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url
        }


    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.reference = self.patient_id.reference

    def action_in_consultation(self):
        if self.state == 'draft':
            self.state = 'in_consultation'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        action = self.env.ref('hospital.action_cancel_appointment').read()[0]
        return action

    def unlink(self):
        for rec in self:
         if rec.state != 'draft':
            raise ValidationError(_("you can delete appintment only in draft status"))
        return super(HospitalAppointment, rec).unlink()


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'Appointment Pharmacy Lines'

    product_id=fields.Many2one('product.product',required=True)
    price_unit=fields.Float(String='Price')
    qty=fields.Integer(string="Quantity",default=1)
    appointment_id = fields.Many2one('hospital.appointment',string='Appointment')

