{
    "name": "Stock Move Line Position",
    "summary": """
        Get line position from purchase or sale order.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Inventory",
    "version": "14.0.1.2.0",
    "license": "AGPL-3",
    "depends": ["stock", "sale_order_line_pos", "purchase_order_line_position"],
    "data": ["views/view_picking_form.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
