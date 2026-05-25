from odoo import models, fields

class HmsDoctors(models.Model):

    _name = 'hms.doctors'
    _description = 'HMS Doctors'
    _rec_name = 'full_name'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    full_name = fields.Char(string='Full Name', compute='_compute_full_name')
    image = fields.Image(string='Image')

    def _compute_full_name(self):
        for record in self:
            record.full_name = f"{record.first_name} {record.last_name}"    