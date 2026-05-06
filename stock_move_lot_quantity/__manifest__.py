# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Move Lot Quantity",
    "summary": """
        Set total stock quantity of lot as default move quantity.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["stock"],
    "data": [
        "views/stock_move_views.xml",
        "views/stock_move_line_views.xml",
        "views/stock_picking_views.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    
}
