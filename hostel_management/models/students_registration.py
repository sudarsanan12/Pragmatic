from odoo import models, fields, api, _
import re
from odoo.exceptions import ValidationError


class StudentRegistration(models.Model):
    _name = "hostel.student"
    _description = "hostel student"
    _rec_name = "name"
   
    name = fields.Char (string = 'First Name', required = True) 
    last_name = fields.Char (string = 'Last Name', required = True)
    email= fields.Char (string = 'Email Address',required = True)
    permanent_address = fields.Char (string = 'Permanent Address')
    date_of_birth = fields.Date (string = 'Date Of Birth')
    city = fields.Char (string = 'City')
    permanent_address = fields.Char (string = 'Permanent Address',required = True)
    date_of_birth = fields.Date (string = 'Date Of Birth',required = True)
    city = fields.Char (string = 'City',required = True)
    user_id = fields.Many2one('res.users')

    make_visible = fields.Boolean(string="User", compute='get_user')


    state = fields.Selection([
    ('select', 'Select'),
    ('andhra_pradesh', 'Andhra Pradesh'),
    ('arunachal_pradesh', 'Arunachal Pradesh'),
    ('assam', 'Assam'),
    ('bihar', 'Bihar'),
    ('chhattisgarh', 'Chhattisgarh'),
    ('goa', 'Goa'),
    ('gujarat', 'Gujarat'),
    ('haryana', 'Haryana'),
    ('himachal_pradesh', 'Himachal Pradesh'),
    ('jharkhand', 'Jharkhand'),
    ('jk', 'Jammu and Kashmir'),
    ('karnataka', 'Karnataka'),
    ('kerala', 'Kerala'),
    ('madhya_pradesh', 'Madhya Pradesh'),
    ('maharastra', 'Maharastra'),
    ('maharashtra', 'Maharashtra'),
    ('manipur', 'Manipur'),
    ('meghalaya', 'Meghalaya'),
    ('mizoram', 'Mizoram'),
    ('nagaland', 'Nagaland'),
    ('odisha', 'Odisha'),
    ('punjab', 'Punjab'),
    ('rajasthan', 'Rajasthan'),
    ('sikkim', 'Sikkim'),
    ('tamil_nadu', 'Tamil Nadu'),
    ('telangana', 'Telangana'),
    ('tripura', 'Tripura'),
    ('uttar_pradesh', 'Uttar Pradesh'),
    ('uttarakhand', 'Uttarakhand'),
    ('west_bengal', 'West Bengal')], required=True, default='select')

    mother_name = fields.Char (string = 'Mother Name', required = True)
    father_name = fields.Char (string = 'Father Name', required = True)
    gender = fields.Selection ([('select','Select'),('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],string = 'Gender', required = True, default='select')
    contact = fields.Char (string = 'Student Contact No', required = True)
    parent_contact = fields.Char (string = 'Parent Contact No', required = True)
    course = fields.Char (string='Course Name', required = True)
    year = fields.Char (string='Year Of Study', required = True)
    semester = fields.Char (string='Semester', required = True)
    sequence = fields.Char(string = 'Sequence', required = True, copy = False, readonly = True,default = lambda self: _('New'))
    states = fields.Selection([('drafted','Drafted'),('confirmed','Confirmed'),('rejected','Rejected')],string='Status',default='drafted')
    space = fields.Char(' ', readonly=True)


    def confirm(self):
        self.states = "confirmed"
        self.sequence = self.env['ir.sequence'].next_by_code('hostel.student.seq') or _('New')

    def reject(self):
        self.states = "rejected"

   
    @api.depends('make_visible')
    def get_user(self, ):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('hostel_management.admin_group'):
            self.make_visible = True
        else:
            self.make_visible = False

    @api.constrains('email')
    def constrains_email(self):
        for record in self:
            if record.email:
                match = re.match('^[_A-Za-z0-9-]+(\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*(\.[A-Za-z]{2,4})$',record.email)
                if match == None:
                    raise ValidationError('Invalid Email')
                
   
    @api.constrains('contact')
    def _validate_contact(self):
        for record in self:
            if record.contact:
                pattern = r'^[789]\d{9}$'
                if not re.match(pattern, record.contact):
                    raise models.ValidationError('Invalid student contact number!')  




    @api.constrains('parent_contact')
    def _validate_contact_number(self):
        for record in self:
            if record.parent_contact:
                pattern = r'^[789]\d{9}$'
                if not re.match(pattern, record.parent_contact):
                    raise models.ValidationError('Invalid parent contact number!')

            