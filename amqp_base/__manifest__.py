{
    "name": "AMQP Base",
    "summary": """
        Manage target hosts for AMQP messages.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Tools",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base"],
    "data": ["security/ir.model.access.csv", "views/amqp.xml", "views/amqp_message.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
