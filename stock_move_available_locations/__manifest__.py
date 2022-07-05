{
    "name": "Stock move available locations",
    "summary": """
        Show storage locations that have a positive stock for the product.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Inventory",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["stock", "web_domain_field"],
    "data": ["views/stock.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
