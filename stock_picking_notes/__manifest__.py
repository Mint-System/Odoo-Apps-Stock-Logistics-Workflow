{
    "name": "Stock Picking Notes",
    "summary": """
        Notes from sale order are copied to stock picking on confirmation.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Inventory",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["stock", "sale_order_notes"],
    "data": ["views/view_picking_form.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}