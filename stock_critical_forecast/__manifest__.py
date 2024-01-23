{
    "name": "Stock Critical Forecast",
    "summary": """
        Show critical demand date for components in manufacturing and products to be shipped.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-workflow",
    "category": "Inventory",
    "version": "17.0.1.0.0",
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
    # "assets": {
    #     "web.assets_backend": [
    #         "stock_critical_forecast/static/src/js/show_last_updated_date.js",
    #     ],
    #     "web.assets_qweb": [
    #         "stock_critical_forecast/static/src/xml/listview_last_updated_date.xml",
    #     ],
    # },
}
