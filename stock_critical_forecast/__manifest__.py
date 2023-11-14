{
    "name": "Stock Critical Forecast",
    "summary": """
        Show critical demand date for components in manufacturing and products to be shipped.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Inventory",
    "version": "14.0.4.6.2",
    "license": "AGPL-3",
    "depends": ["mrp", "sale_stock", "product_type_description"],
    "data": [
        "security/ir.model.access.csv",
        "views/critical_forecast_views.xml",
        "wizard/critical_forecast_views.xml",
        "data/ir_cron.xml",
    ],
    "qweb": ["static/src/xml/listview_last_updated_date.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
