from datetime import date, datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta



class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"
    _rec_name = 'name'

    name = fields.Char(string='Name', tracking=True)
    date_of_birth = fields.Date(string='Date Of Birth')
    reference = fields.Char(string='Reference')
    age = fields.Integer(string="Age", compute='_compute_age', inverse='_inverse_compute_age', search='_search_age', store=True)
    phone = fields.Integer(string="Phone")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True, default='female')
    active = fields.Boolean(string="Active", default=True)
    appointment_id = fields.Many2one('hospital.appointment', string="Appointments")
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string='Tags')

    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital Status", tracking=True,
                                      default='single')
    partner_name = fields.Char(string="Partner Name")
    is_birthday = fields.Boolean(string="birthday ?", compute='_compute_is_birthday')

    @api.constrains('date_of_birth')
    def check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("The entered date of birth is not acceptable"))

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                today = date.today()
                rec.age = today.year - rec.date_of_birth.year - ((today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
            else:
                rec.age = 0

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)


    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    @api.ondelete(at_uninstall=False)
    def check_appointment(self):
        for rec in self:
            if rec.appointment_id:
                raise ValidationError(_("You can't delete a patient with appointments"))

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('hospital.patient')
        vals['reference'] = sequence
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        if not vals.get('reference'):
            sequence = self.env['ir.sequence'].next_by_code('hospital.patient')
            vals['reference'] = sequence
        return super(HospitalPatient, self).write(vals)

   # search non store value this way

    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1,month=1)
        end_of_year = date_of_birth.replace(day=30, month=12)
        print("start....", start_of_year)
        print("start....", end_of_year)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False  # Initialize a boolean variable to False by default
            if rec.date_of_birth:  # Check if the date of birth is not empty
                today = date.today()  # Get today's date
                # Check if today's day and month match the day and month of the date of birth
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True  # Set is_birthday to True if it's the person's birthday
            rec.is_birthday = is_birthday  # Assign the value of is_birthday to the field is_birthday in the record



