{
    "name": "Stock Critical Forecast",
    "summary": """
        Show critical demand date for components in manufacturing and products to be shipped.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Inventory",
    "version": "14.0.1.1.1",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        "purchase_stock",
        "sale_stock",
        "sale_blanket_order",
        "product_type_description",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/critical_forecast_views.xml",
    ],
    "qweb": ["static/src/xml/action_refresh_button.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
}
