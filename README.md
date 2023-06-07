# Odoo Apps: Stock Logistics Workflow

Collection of stock model related modules.

## Usage

Clone module into Odoo addon directory.

```bash
git clone git@github.com:mint-system/odoo-apps-stock-logistics-workflow.git ./addons/stock_logistics_workflow
```

## Available modules

| Module | Summary |
| --- | --- |
| [stock_account_location_valued](stock_account_location_valued) |         Mark stock location to be valued. |
| [stock_aggregated_move_line](stock_aggregated_move_line) |         Access move line in stock aggregated report. |
| [stock_aggregated_move_lines_description](stock_aggregated_move_lines_description) |         Use stock move description for the aggregated move line description. |
| [stock_barcode_mrp](stock_barcode_mrp) |         Access work order by scanning the barcode of a manufacturing order. |
| [stock_barcode_packaging](stock_barcode_packaging) |         Show sale order packaging on barcode operation. |
| [stock_critical_forecast_link_replenish](stock_critical_forecast_link_replenish) |         Calculate action date from active orderpoint rules. |
| [stock_critical_forecast](stock_critical_forecast) |         Show critical demand date for components in manufacturing and products to be shipped. |
| [stock_critical_forecast_promised_agreed](stock_critical_forecast_promised_agreed) |         Extends report with agreed and promised quantity. |
| [stock_forecasted_report_min_qty](stock_forecasted_report_min_qty) |         Include minimum stock in forecast. |
| [stock_inventory_summary](stock_inventory_summary) |     "installable": True, |
| [stock_move_available_locations](stock_move_available_locations) |         Show storage locations that have a positive stock for the product. |
| [stock_move_line_lot_done](stock_move_line_lot_done) |         When lot is assigned automatically set quantity done. |
| [stock_move_line_packaging](stock_move_line_packaging) |         Link product packaging from sale order. |
| [stock_move_line_position](stock_move_line_position) |         Get line position from purchase, sale or manufacturing order. |
| [stock_move_sale_order_name](stock_move_sale_order_name) |         Use sale order line name for stock move description. |
| [stock_move_upstream_quantity](stock_move_upstream_quantity) |         Propagate quantity done change on stock move to upstream moves. |
| [stock_move_upstream_state](stock_move_upstream_state) |         Access state of upstream move in current move. |
| [stock_move_weight_uom](stock_move_weight_uom) |         Convert unit of measurement when calculating total weight. |
| [stock_picking_mrp_production_assign](stock_picking_mrp_production_assign) |         Assign picking and upstream manufacture order at the same time. |
| [stock_picking_mrp_production_done](stock_picking_mrp_production_done) |         Complete picking and upstream manufacture order at the same time. |
| [stock_picking_notes](stock_picking_notes) |         Notes from sale order are copied to stock picking on confirmation. |
| [stock_picking_responsible](stock_picking_responsible) |         Use sale order user stock picking responsible. |
| [stock_production_lot_date](stock_production_lot_date) |         Define lot date and set expiry date relatively. |
| [stock_production_lot_qty_storable](stock_production_lot_qty_storable) |         Store value of product qty of lot. |
| [stock_product_last_move](stock_product_last_move) |         Show last incoming and outgoing move date of product. |
