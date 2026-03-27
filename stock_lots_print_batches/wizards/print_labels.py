import io
import zipfile
import base64

from odoo import models, fields, api

class PrintSerialLabelsWizard(models.TransientModel):
    _name = 'print.serial.labels.wizard'
    _description = 'Print Serial Labels in Batches'

    batch_size = fields.Integer(
        string='Batch Size',
        default=30,
        required=True,
        help='Number of labels per PDF file'
    )

    def action_print_labels(self):
        """Print selected serials in batches of chosen size"""
        active_ids = self.env.context.get('active_ids')
        lots = self.env['stock.lot'].browse(active_ids)
        if not lots:
            return

        batch_size = self.batch_size
        if batch_size <= 0:
            batch_size = 30

        # Create ZIP if more than one batch
        if len(lots) > batch_size:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zf:
                for i in range(0, len(lots), batch_size):
                    batch = lots[i:i + batch_size]
                    batch_num = i // batch_size + 1
                    total_batches = (len(lots) + batch_size - 1) // batch_size

                    # Generate PDF for this batch
                    report = self.env.ref('stock.action_report_lot_label')
                    pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(report.report_name, res_ids=batch.ids)

                    # Add batch info to filename
                    filename = f"Serial_Labels_Batch_{batch_num}_of_{total_batches}.pdf"
                    zf.writestr(filename, pdf_content)


            attachment = self.env["ir.attachment"].create({
                "name": "Serial_Labels_Batches.zip",
                "datas": base64.b64encode(zip_buffer.getvalue()),
                "res_model": "stock.lot",
                "res_id": lots[0].id,
            })
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'target': 'self',
                'next': {
                    'type': 'ir.actions.act_window_close',
                }
            }


        else:
            # Single batch — just print
            return self.env.ref('stock.action_report_lot_label').report_action(lots)

