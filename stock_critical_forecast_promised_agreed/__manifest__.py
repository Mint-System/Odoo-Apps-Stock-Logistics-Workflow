{
    "name": "Stock Critical Forecast Promised Agreed",
    "summary": """
        Extends report with agreed and promised quantity.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Inventory",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "product",
        "stock_critical_forecast",
        "purchase_requisition",
        "sale_blanket_order",
    ],
    "data": ["views/critical_forecast_views.xml"],
    "demo": ["data/sale_blanket_order_demo.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
