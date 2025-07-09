{
    "name": "hr_holidays_extend",
    "version": "1.0",
    "website": "https://kienodoo.com",
    "author": "KienOdoo",
    "description": """
        hr_holidays_extend module
    """,
    "category": "Sales",
    "depends": ["base", "hr"],
    "data": [
        'security/ir.model.access.csv',
        'wizards/leave_batchupdate_wizard_views.xml',
        'views/hr_leave_extend_views.xml',
    ],
    "installable": True,
    "application": True,
    "license":"LGPL-3"
}
