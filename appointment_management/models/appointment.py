# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Appointment(models.Model):
    _name = 'hospital.appointment'
    _rec_name = "name"

    name = fields.Char('Appointment Number', default=lambda self: self.env['ir.sequence'].next_by_code('hospital.appointment'))
    appointment_date = fields.Datetime('Accepted Appointment Date')
    doctor_id = fields.Many2one('res.doctor', string="Doctor Name", default=lambda self: self.env.user.doctor_id)
    patient_id = fields.Many2one('res.patient', string="Patient Name", default=lambda self: self.env.user.patient_id)
    appointment_status = fields.Selection([('New','New'),('Accepted','Accepted'),('Rejected','Rejected')],
                                          string='Appointment Status', default='New')
    reason = fields.Char('Symptoms/Reasons')
    rejection_reason = fields.Char('Reason for Appointment Rejection')

    @api.multi
    def approve_appointment(self):
        view_id = self.env['appointment.approval.reject.wizard']
        ctx = dict()
        ctx.update({
            'default_model': 'hospital.appointment',
            'default_res_id': self.ids[0],
            'default_appointment_id': self.id,
            'default_doctor_id': self.doctor_id.id,
            'default_patient_id': self.patient_id.id,
            'default_appointment_status': 'Accepted'
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment Approval',
            'res_model': 'appointment.approval.reject.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('appointment_management.appointment_approval_confirm_wizard', False).id,
            'target': 'new',
            'context': ctx
        }

    @api.multi
    def reject_appointment(self):
        view_id = self.env['appointment.approval.reject.wizard']
        ctx = dict()
        ctx.update({
            'default_model': 'hospital.appointment',
            'default_res_id': self.ids[0],
            'default_appointment_id': self.id,
            'default_doctor_id': self.doctor_id.id,
            'default_patient_id': self.patient_id.id,
            'default_appointment_status': 'Rejected'
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment Rejection',
            'res_model': 'appointment.approval.reject.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('appointment_management.appointment_rejection_confirm_wizard', False).id,
            'target': 'new',
            'context': ctx
        }

class InheritedResUsers(models.Model):
    _inherit = "res.users"

    doctor_id = fields.Many2one('res.doctor', string="Doctor Name")
    patient_id = fields.Many2one('res.patient', string="Patient Name")

    def _get_groups(self, existing_user_base_groups, groups):
        group_ids = existing_user_base_groups
        for g in groups:
            group = self.env.ref(g, raise_if_not_found=False)
            if group:
                group_ids.append(group.id)
        return [[6, False, group_ids]]
