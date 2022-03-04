# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re


class ResDoctor(models.Model):
    _name = 'res.doctor'
    _description = 'Doctor'
    _rec_name = "name"

    name = fields.Char('Doctor Name', required=1, size=20)
    company_id = fields.Many2one('res.company', string='Hospital', default=lambda self: self.env.user.company_id)
    mobile = fields.Char('Mobile', size=10)
    mobile_country_code = fields.Char(readonly=1, default='91')
    email = fields.Char('Email')
    street = fields.Char('street')
    city = fields.Char('city')
    zip = fields.Char('Zip',size=6)
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')
    user_id = fields.Many2one('res.user', string='User ID')
    user_created = fields.Boolean(default=False)

    @api.constrains('mobile')
    def validate_mobile(self):
        if self.mobile:
            match_mobile = re.match('^[\d]*$', self.mobile)
            if not match_mobile or len(self.mobile) != 10:
                raise ValidationError('Please enter a valid 10 digit mobile number.')
            return True
        else:
            return False

    @api.constrains('email')
    def validate_email(self):
        email = str(self.email.lower())
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
        if not match:
            raise ValidationError('Please enter a valid email address!')

    @api.multi
    def create_user(self):
        if not self.user_id:
            groups_id = self.env['res.users']._get_groups([], ['appointment_management.group_doctor', 'base.group_user'])
            user_obj = self.env['res.users'].sudo().create({
                'login': self.email,
                'name': self.name,
                'middle_name': ' ',
                'last_name': ' ',
                'mobile': self.mobile,
                'email': self.email,
                'company_id': self.company_id.id,
                'company_ids': [(6, 0, [self.company_id.id])],
                'groups_id': groups_id,
                'doctor_id': self.id,
                'password': self.name
            })
            user_obj.partner_id.sudo().write({'company_id': user_obj.company_id.id})
            self.user_id = user_obj.id
            self.user_created = True
        else:
            raise ValidationError("The user is already created for %s" % self.name)
