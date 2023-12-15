from odoo import models, fields, api


class Users(models.Model):
    _inherit = 'res.users'
    _description = 'IsAdmin'


    student = fields.Boolean(string='Is Student')
    admin = fields.Boolean(string='Is Admin')

    @api.model
    def create(self, vals):
        # Create the user
        user = super(Users, self).create(vals)            
        if user.student:
            student_login_group = self.env.ref('hostel_management.students_group')
            # Check if the group exists and assign it to the user
            if student_login_group:
                user.write({'groups_id': [(4, student_login_group.id)]})
        elif user.admin:
            admin_login_group = self.env.ref('hostel_management.admin_group')
            if admin_login_group:
                user.write({'groups_id': [(4, admin_login_group.id)]})

        return user

    
    def write(self, vals):
        # Check if the student field is being modified
        print(vals)
        if 'student' in vals:
            student_login_group = self.env.ref('hostel_management.students_group')
            if vals['student']:
                    # Add the user to the students_group
                if student_login_group:
                    self.write({'groups_id': [(4, student_login_group.id)]})
            else:
                # Remove the user from the students_group
                if student_login_group and student_login_group in self.groups_id:
                    self.write({'groups_id': [(3, student_login_group.id)]})
        if 'admin' in vals:
            admin_login_group = self.env.ref('hostel_management.admin_group')
            if vals['admin']:
                # Add the user to the admin_group
                if admin_login_group:
                    self.write({'groups_id': [(4, admin_login_group.id)]})
            else:
            # Remove the user from the admin_group
                if admin_login_group and admin_login_group in self.groups_id:
                    self.write({'groups_id': [(3, admin_login_group.id)]})
        return super(Users, self).write(vals)



    


    