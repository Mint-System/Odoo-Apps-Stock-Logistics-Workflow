# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Critical Forecast Compare",
    "summary": """
        Calculate critical forecast
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["mrp", "stock", "sale_stock", "purchase"],
    "data": [
        "security/ir.model.access.csv",
        "views/critical_forecast_views.xml",
        "data/ir_cron.xml",
        "wizard/critical_forecast_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    
}
