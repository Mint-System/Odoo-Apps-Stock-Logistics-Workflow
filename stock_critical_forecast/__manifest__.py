{
    "name": "Stock Critical Forecast",
    "summary": """
        Show critical demand date for components in manufacturing and products to be shipped.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Inventory",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["mrp", "sale_stock", "purchase"],
    "data": [
        "security/ir.model.access.csv",
        "views/critical_forecast_views.xml",
        "data/ir_cron.xml",
        "wizard/critical_forecast_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
