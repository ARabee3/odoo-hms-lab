from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'HMS Patient'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ], string='Blood Type')
    pcr = fields.Boolean(string='PCR')
    image = fields.Image(string='Image')
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    email = fields.Char(string='Email')

    # New fields for Lab 02
    department_id = fields.Many2one(
        'hms.department',
        string='Department',
        domain=[('is_opened', '=', True)],
    )
    doctor_ids = fields.Many2many('hms.doctors', string='Doctors')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], string='State', default='undetermined')
    capacity = fields.Integer(
        related='department_id.capacity',
        string='Department Capacity',
        readonly=True,
        store=True,
    )
    log_history_ids = fields.One2many(
        'hms.patient.log',
        'patient_id',
        string='Log History',
    )

    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                today = fields.Date.today()
                patient.age = today.year - patient.birth_date.year - (
                    (today.month, today.day) < (patient.birth_date.month, patient.birth_date.day)
                )
            else:
                patient.age = 0

    @api.constrains('email')
    def _check_email(self):
        for patient in self:
            if patient.email:
                if not tools.email_validate(patient.email):
                    raise ValidationError('Please enter a valid email address.')
                # Check uniqueness
                existing = self.env['hms.patient'].search([
                    ('email', '=', patient.email),
                    ('id', '!=', patient.id),
                ])
                if existing:
                    raise ValidationError('This email address already exists in another patient record.')

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30 and not self.pcr:
            self.pcr = True
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'PCR has been automatically checked because age is less than 30.',
                }
            }

    @api.model_create_multi
    def create(self, vals_list):
        patients = super(HmsPatient, self).create(vals_list)
        for patient in patients:
            state_label = dict(self._fields['state'].selection).get(patient.state)
            self.env['hms.patient.log'].create({
                'patient_id': patient.id,
                'description': f'State changed to {state_label}',
            })
        return patients

    def write(self, vals):
        res = super(HmsPatient, self).write(vals)
        if 'state' in vals:
            for patient in self:
                state_label = dict(self._fields['state'].selection).get(patient.state)
                self.env['hms.patient.log'].create({
                    'patient_id': patient.id,
                    'description': f'State changed to {state_label}',
                })
        return res
