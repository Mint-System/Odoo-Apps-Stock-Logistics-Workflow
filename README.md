# Odoo Apps: Stock Logistics Workflow

Collection of stock model related modules.

## Usage

Clone module into Odoo addon directory.

```bash
git clone git@github.com:mint-system/odoo-apps-stock-logistics-workflow.git ./addons/stock_logistics_workflow
```

## Available modules

| Module                                                  | Summary                                                                               |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [stock_move_line_position](stock_move_line_position/)   | Get line position from purchase or sale order.                                        |
| [stock_move_line_packaging](stock_move_line_packaging/) | Link product packaging from sale order.                                               |
| [stock_barcode_packaging](stock_barcode_packaging/)     | Show sale order packaging on barcode operation.                                       |
| [stock_move_weight_uom](stock_move_weight_uom/)         | Convert unit of measurement when calculating total weight.                            |
| [stock_critical_forecast](stock_critical_forecast/)     | Show critical demand date for components in manufacturing and products to be shipped. |
