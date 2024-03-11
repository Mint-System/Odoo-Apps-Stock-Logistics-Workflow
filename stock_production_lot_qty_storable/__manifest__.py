{
    "name": "Stock Production Lot Qty Storable",
    "summary": """
        Store value of product qty of lot.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Inventory",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["stock"],
    "data": ["views/stock_production_lot.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "qweb": ["static/src/xml/board.xml"],
}
