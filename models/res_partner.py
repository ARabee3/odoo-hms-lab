from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient')

    @api.constrains('email', 'related_patient_id')
    def _check_patient_email(self):
        for partner in self:
            if partner.related_patient_id and partner.email:
                existing = self.env['hms.patient'].sudo().search([
                    ('email', '=', partner.email),
                    ('id', '!=', partner.related_patient_id.id),
                ])
                if existing:
                    raise ValidationError(
                        f'This email ({partner.email}) already exists in the patient records. '
                        'You cannot link a customer with an email that already belongs to a patient.'
                    )

    def unlink(self):
        for partner in self:
            if partner.related_patient_id:
                raise ValidationError(
                    'You cannot delete a customer that is linked to a patient.'
                )
        return super(ResPartner, self).unlink()
