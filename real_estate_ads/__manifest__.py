{
    "name": "Real estate ads",
    "version": "1.0",
    "website": "https://kienodoo.com",
    "author": "KienOdoo",
    "description": """
        Real estate ads module
    """,
    "category": "Sales",
    "depends": ["base"],
    "data": [
        'security/ir.model.access.csv',
        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_tag_view.xml',
        'views/menu_items.xml',

        # data files
        'data/property_type.xml',
        'data/estate.property.type.csv',
    ],
    "demo":[
        'demo/property_tag.xml'
    ],
    "installable": True,
    "application": True,
    "license":"LGPL-3"
}
