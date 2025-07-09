{
    "name": "Performance Review Management",
    "version": "1.0",
    "website": "https://kienodoo.com",
    "author": "KienOdoo",
    "description": """
        Performance Review Management Module
    """,
    "category": "Sales",
    "depends": ["base","hr"],
    "data": [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/hr_performance_review_view.xml',
        'views/hr_employee_experience_wizard_view.xml',
        'views/wizards/employees_experience_year_wizard_view.xml',
        'views/hr_employee.xml',
        'views/menus.xml',
    ],
    "demo": ["demo/hr_performance_review.xml"],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
