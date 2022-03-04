# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import datetime
import calendar


class ApprovalRejectConfirmwizard(models.TransientModel):
    _name = 'appointment.approval.reject.wizard'

    appointment_id = fields.Many2one('hospital.appointment')
    appointment_status = fields.Selection([('New', 'New'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')],
                                          string='Appointment Status')
    appointment_date = fields.Datetime('Accepted Appointment Date')
    rejection_reason = fields.Char('Reason for Appointment Rejection')
    doctor_id = fields.Many2one('res.doctor', string="Doctor Name")
    patient_id = fields.Many2one('res.patient', string="Patient Name")

    @api.multi
    def approval_action_confirm(self):
        app_id = self.env.context.get('active_id')
        if self.appointment_date:
            for rec in self.env['hospital.appointment'].sudo().search([('appointment_status','=','Accepted'),('doctor_id','=', self.doctor_id.id)]):
                appt_time = datetime.datetime.strptime(self.appointment_date, '%Y-%m-%d %H:%M:%S')
                st_time = datetime.datetime.strptime(rec.appointment_date, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(minutes=15)
                ed_time = datetime.datetime.strptime(rec.appointment_date, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=15)
                if appt_time >= st_time and appt_time <= ed_time:
                    raise ValidationError('sorry other appointment was in the proposed timeinterval')
            self.appointment_id.appointment_status = 'Accepted'
            self.appointment_id.appointment_date = self.appointment_date

    @api.multi
    def rejection_action_confirm(self):
        app_id = self.env.context.get('active_id')
        self.appointment_id.appointment_status = 'Rejected'
        self.appointment_id.rejection_reason = self.rejection_reason