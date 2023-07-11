{
    "name": "Stock Barcode Maintenance",
    "summary": """
        Scan barcodes to show maintenance equipments.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Inventory",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["maintenance", "stock_barcode"],
    "data": ["views/maintenance_equipment.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
