# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Picking Split And Validate",
    "summary": """
        Splits the picking with respect to a product property and automatically validates the associated picking.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["stock"],
    "data": [
        "views/product_template_views.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    
}
