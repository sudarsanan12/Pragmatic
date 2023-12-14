# -*- coding: utf-8 -*-
{
    'name': "pragmatic_laundry_management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_sale','mail', 'hr','sale','contacts','stock','portal'],

    # always loaded
    'data': [
        'security/laundry_security.xml',
        'security/ir.model.access.csv',
        'views/email_template.xml',
        'views/email_template_delivery_order.xml',
        'views/email_template_cleaner_order.xml',
        'views/email_template_qc_order.xml',
        'wizard/wizard_qc_reject.xml',
        'wizard/driver_delivery_wizard.xml',
        'views/quality_control.xml',
        'data/service.xml',
        'data/ir_sequence_data.xml',
        'views/complaint.xml',
        'views/complaint_web.xml',
        'views/review_web.xml',
        'views/sale_order_inherit_views.xml',
        'views/review_views.xml',
        'views/employee_views.xml',
        'views/driver_dashboard.xml',
        'views/customer_view.xml',
        'views/service_views.xml',
        'views/cleaner_dashboard_views.xml',
        'views/menu.xml',
        'views/company_inherit.xml',
        'views/website.xml',
        'views/web_status_inherit.xml',
        'views/stock.xml',

    ],


}





