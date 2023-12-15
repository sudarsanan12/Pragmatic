
from odoo import models, fields


class Present(models.Model):
    _name = 'hostel.attendance.status'
    _description = "attendance.status"
    _rec_name='id'
    

    student_id = fields.Many2one('hostel.student')
    first_name = fields.Char(related='student_id.name')
    last_name = fields.Char(related='student_id.last_name')
    present = fields.Boolean(string="Present")
    attendance_id = fields.Many2one('hostel.attendance')


class HostelAttendance(models.Model):
    _name = 'hostel.attendance'
    _description = 'Attendance'
    _rec_name='date'


    attendance_lines = fields.One2many('hostel.attendance.status','attendance_id')
    date = fields.Date(string='Date', required=True)

    def all_students(self):
        lis = []
        students = self.env['hostel.student'].search([('states', '=', 'confirmed')])
        for records in students:
            student = self.env['hostel.attendance.status'].create(
            {
                'student_id':records.id,
            })
            lis.append(student.id)
        self.attendance_lines = [(6,0, lis)]
