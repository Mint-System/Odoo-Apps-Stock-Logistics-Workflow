{
    "name": "Stock Critical Forecast",
    "summary": """
        Show critical demand date for components in manufacturing and products to be shipped.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Inventory",
    "version": "14.0.2.0.0",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        "sale_stock",
        "product_type_description",
        "purchase_requisition",
        "sale_blanket_order",
    ],
    "data": ["security/ir.model.access.csv", "views/critical_forecast_views.xml"],
    "qweb": ["static/src/xml/listview_refresh.xml"],
    "demo": ["data/sale_blanket_order_demo.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
