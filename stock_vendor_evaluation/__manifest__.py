{
    "name": "Stock Vendor Evaluation",
    "summary": """
        Rate each receipt and analyze vendor ratings.
    """,
    "author": "Mint System GmbH",
    "website": "https://github.com/OCA/sale-workflow",
    "category": "Inventory",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["purchase_stock", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/view_picking_form.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
