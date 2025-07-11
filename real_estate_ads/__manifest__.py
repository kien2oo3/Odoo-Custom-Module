{
    "name": "Real estate ads",
    "version": "1.0",
    "website": "https://kienodoo.com",
    "author": "KienOdoo",
    "description": """
        Real estate ads module
    """,
    "category": "Sales",
    "depends": ["base", "mail", "website"],
    "data": [
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "security/model_access.xml",
        "security/ir_rule.xml",
        "views/property_view.xml",
        "views/property_type_view.xml",
        "views/property_tag_view.xml",
        "views/property_offer_view.xml",
        "views/menu_items.xml",
        "views/res_users_views_extend.xml",
        # data files
        "data/property_type.xml",
        "data/estate.property.type.csv",
    ],
    "demo": ["demo/property_tag.xml"],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
