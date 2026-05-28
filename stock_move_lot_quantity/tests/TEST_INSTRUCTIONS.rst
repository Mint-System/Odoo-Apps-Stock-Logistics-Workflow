Configuration:

- Go to Inventory > Configuration.
- In > Settings enable "Lots & Serial Numbers", "Storage Locations" and "Multi-Step Routes".
- Open configuration for your warehouse and enable "Pick components then manufacture (2 steps)" for "Manufature".
- Create a Pre-Production Location with "WH/Stock" as parent. 
- Chose this location as source location for operation type "Manufacture".
- Chose this location as destination location for operation type "Pick Components".
- Set reservation method of operation types "Manufacture" and "P{ick Components" to "At Confirmation".

Products:

- Create products "A" a "A1" where "A1" is tracked by lot.
- Create two lots "Lot1" and "Lot2" for product "A1" with stock of 20 units each.

Manufacturing:

- Go to Manufacturing App and create BoM for Product "A" with "A1" as Component (quantity: 5).
- Create new MO for 3 units of product "A". 
- Follow "Transfer" Button and check if "Lot1" is picked.
- Create second MO for 3 units of "A".
- Check that "Lot1" and "Lot2" are picked.
- Now Validate Picking of the first MO.
- Check the moves of picking for second MO.
- By validating picking of first MO total stocks of "Lot1" was moved to pre-production location.
- Picking for second MO now transfers "Lot2" from Stock and "Lot1" from pre-production because "Lot1" was moved to pre-production location when validated.