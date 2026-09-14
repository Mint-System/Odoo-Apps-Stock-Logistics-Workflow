from odoo import models


class CriticalForecastComputeWizard(models.TransientModel):
    _name = "critical.forecast.compute.wizard"
    _description = "Trigger recomputation of Critical Forecast Lines"

    def calculate(self):
        self.env["critical.forecast.line"].get_data()
        return {"type": "ir.actions.client", "tag": "reload"}