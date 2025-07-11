{
    "name": "Attendance management",
    "version": "1.0",
    "website": "https://kienodoo.com",
    "author": "KienOdoo",
    "description": """
        Attendance management module
    """,
    "category": "Sales",
    "depends": ["base", "hr"],
    "data": [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/attendance_request_views.xml',
        'views/menu_items.xml'
    ],
    "installable": True,
    "application": True,
    "license":"LGPL-3"
}
