{
    "name": "AMQP Stock",
    "summary": """
        Consume and publish stock operations as AMQP messages.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Tools",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["amqp_base","stock"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "external_dependencies": {"python": ["pika"]},
}
