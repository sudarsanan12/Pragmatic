from odoo import models, fields,api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import pytz
from datetime import datetime


class HostelVisitors(models.Model):
    _name = 'hostel.visitors'
    _description = 'Visitors'

    name = fields.Char(string = "Visitor Name", required=True)
    seq = fields.Char(string="Id", default="New")
    address = fields.Char(string = "Address")
    contact = fields.Char(string= "Contact number", required=True)
    student_id = fields.Many2one('hostel.student', required=True)
    relation = fields.Selection([('father', 'Father'), ('mother', 'Mother'),
                                ('sister', 'Sister'),('brother', 'Brother'),('others', 'Others')], string='Relation With The student', required=True)
    time_from = fields.Datetime(string="Select time from (only after 9 AM)",required=True)
    time_to = fields.Datetime(string="Select time to (only before 7PM)",required=True)
    time = fields.Char(compute="compute_time", store=True)
    reason = fields.Char(string = "Reason to meet ")
    state = fields.Selection([('pending', 'Pending'), ('rejected', 'Rejected'),
                                ('approved', 'Approved')], string='Status', default ="pending")
    company_user = fields.Many2one('res.company', string="Company")


    @api.model
    def create(self, vals):
        vals['seq'] = self.env['ir.sequence'].next_by_code('hostel.visitors')
        return super(HostelVisitors, self).create(vals)

    def approve(self):
        self.state = "approved"

    def reject(self):
        self.state = "rejected"
        
    
    @api.onchange('time_from', 'time_to', 'contact', 'student_id')
    def validations_for_visitors(self):
        if self.time_from != False:
            for rec in self:
                user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
                from_time = pytz.utc.localize(rec.time_from).astimezone(user_tz)
                today = datetime.now().strftime('%d:%m:%y')
                if from_time.strftime('%d:%m:%y') != today:
                    raise ValidationError('The date must be today')
                time_1 = from_time.strftime('%H')
                if int(time_1) < 9:
                    raise ValidationError('Time must be after 9AM...')
                
        if self.time_to != False:
            for rec in self:
                user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
                to_time = pytz.utc.localize(rec.time_to).astimezone(user_tz)
                today = datetime.now().strftime('%d:%m:%y')
                if to_time.strftime('%d:%m:%y') != today:
                    raise ValidationError('The date must be today')
                time_2 = to_time.strftime('%H')
                if int(time_2) > 18:
                    raise ValidationError('Time must be before 7PM...')

        if self.contact != False:     
            if len(self.contact) != 10:
                raise ValidationError("Contact number Should be 10 digit.....")
            try :
                int(self.contact)
            except:
                raise ValidationError("Numbers Only allowed.....!!!")



    @api.depends('time_from', 'time_to')
    def compute_time(self):
        for rec in self:
            delta = relativedelta(rec.time_to, rec.time_from)
            rec.time = f"{delta.hours} Hours and {delta.minutes} Minutes"
