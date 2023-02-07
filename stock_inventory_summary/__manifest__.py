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
    "depends": ["mrp", "sale_stock", "product_type_description"],
    "data": ["security/ir.model.access.csv", "views/inventory_summary.xml",],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
