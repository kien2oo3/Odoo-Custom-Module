{
    "name": "Leave management",
    "version": "1.0",
    "website": "https://kienodoo.com",
    "author": "KienOdoo",
    "description": """
        Leave management module
    """,
    "category": "Sales",
    "depends": ["base"],
    "data": [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.xml',
        'views/leave_request_view.xml',
        'views/menuitems.xml'
    ],
    "installable": True,
    "application": True,
    "license":"LGPL-3"
}
