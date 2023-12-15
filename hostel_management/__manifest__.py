# -*- coding: utf-8 -*-
{
    'name': "hostel_management",

    'summary': """ This is a design and implementation of a Hostel Management system.
    For the past few years the number of educational institutions is increasing rapidly.
    Thereby the number of hostels is also increasing for the accommodation of the students studying in this institution.
    This particular project deals with the problems on managing a hostel and avoids the problems which occur when carried manually. 
        
        """,

    'description': """
        The main objective of the Hostel Management System is to manage the details of the students Rent, Allotment of the rooms,Types of Rooms, Payments.
        It manages all the information about Rent, Beds, Payments, Rent.

        Student Management

        Admin can control and update all the activities happening in other modules
        Using student login students can update the student details,seek help regarding maintenance with the admin 

        Student Registration

        In this project students have the option to login into their account using the student registration form

        Student Login
        In this section students log in with their email id and password.

        Room Allocation

        Different types of rooms are available. Students can select the types by logging with their user credentials.

    
        Visitor Management

        In this section visitor details can be seen.
                Visitor Registration (Only parents of registered students)
                        Hostel Timings

                


    """,

    'author': "My Hostel",
    'website': "http://www.yourhostel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly


    'depends': ['base','website'],
    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/maintenance.xml',
        'views/attendance.xml',
        'views/room_view.xml',
        'views/templates.xml',
        'views/help_desk.xml',
        'views/visitors_management.xml',
        'views/student_registration_views.xml',
        'views/bills.xml',        
        'views/inventory_management.xml',
        'views/user.xml',
        'reports/bills_report.xml',       
        'reports/visitor_report.xml',
        'views/staff_management.xml',
        'reports/maintenance_report.xml',
        'reports/staff_management_report.xml',         
        'views/room_allocation.xml',  
        'views/stock_management.xml',      
        'data/ir_sequence_data.xml',
        'views/contact.xml',
        'views/menu_view.xml',   
        'views/registration_template.xml',
        'views/register_form.xml',
        'views/homepage.xml',

        
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

