{
    "name": "Stock Inventory Summary",
    "summary": """
        Presents stock inventory data grouped by location and product.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Inventory",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["stock"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/inventory_summary_history.xml",
        "views/inventory_summary.xml",
        "views/assets.xml",
    ],
    "qweb": ["static/src/xml/inventory_summary.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
