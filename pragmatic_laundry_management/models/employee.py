# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Employee(models.Model):
    _inherit = 'hr.employee'

    is_admin = fields.Boolean(string="Admin",default=False)
    is_driver = fields.Boolean(string="Driver",default=False)
    is_qc = fields.Boolean(string="QC",default=False)
    is_cleaner = fields.Boolean(string="Cleaner",default=False)

    
    def create_users_employee(self):
        if self.is_admin:
            admin_login_group = self.env.ref('pragmatic_laundry_management.group_admin')
            user = self.env['res.users'].create({
            'name': self.name,
            'login': self.work_email,  
            'email': self.work_email,
            'groups_id': [(4, admin_login_group.id)] 
            })
            user.partner_id.is_admin = True
        elif self.is_driver:
            driver_login_group = self.env.ref('pragmatic_laundry_management.group_driver')
            user = self.env['res.users'].create({
            'name': self.name,
            'login': self.work_email,  
            'email': self.work_email,
            'groups_id': [(4, driver_login_group.id)]
            
            })
            user.partner_id.is_driver = True
        elif self.is_qc:
            qc_login_group = self.env.ref('pragmatic_laundry_management.group_qc')
            user = self.env['res.users'].create({
            'name': self.name,
            'login': self.work_email,  
            'email': self.work_email,
            'groups_id': [(4, qc_login_group.id)]
            
            })
            user.partner_id.is_qc = True

        elif self.is_cleaner:
            cleaner_login_group = self.env.ref('pragmatic_laundry_management.group_cleaner')
            user = self.env['res.users'].create({
            'name': self.name,
            'login': self.work_email,  
            'email': self.work_email,
            'groups_id': [(4, cleaner_login_group.id)]
            
            })
            user.partner_id.is_cleaner = True

        self.user_id = user.id
        return user


       