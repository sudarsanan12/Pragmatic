from odoo import models,fields,api
import re
from odoo.exceptions import ValidationError


class HostelStaff(models.Model):
    _name = 'hostel.staff'
    _description = 'hostel.staff'


    name = fields.Char (string = 'Full name', required=True) 
    email = fields.Char (string = 'Email', required=True) 
    address = fields.Char (string = 'Address', required=True)
    city = fields.Char (string = 'City', required=True)
    state = fields.Selection ([('kerala','Kerala'),
    ('goa','Goa'),
    ('maharastra','Maharastra'),
    ('JK','Jammu and Kashmir'),
    ])    
    contact = fields.Char (string = 'Contact', required=True)
    DOB = fields.Date (string = 'Date of birth', required=True)
    gender = fields.Selection ([('Male', 'Male'), ('Female', 'Female')],string = 'Gender')
    marital_status = fields.Selection ([('single','Single'),
    ('married','Married'),
    ('divorced','Divorced'),])    
    monthly_salary = fields.Char (string = 'Monthly Salary', required=True)

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




    

