{
    "name": "Stock Move Line Position",
    "summary": """
        Get line position from purchase or sale order.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Inventory",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["stock", "sale_order_line_position", "purchase_order_line_position"],
    "data": ["views/stock_picking.xml", "views/report_delivery_document.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
