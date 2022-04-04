{
    "name": "Stock Barcode Packaging",
    "summary": """
        Show sale order packaging on barcode operation.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Inventory",
    "version": "14.0.1.0.1",
    "license": "OPL-1",
    "depends": ["stock_barcode", "stock_move_line_packaging"],
    "qweb": ["static/src/xml/stock_barcode_lines_template.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
