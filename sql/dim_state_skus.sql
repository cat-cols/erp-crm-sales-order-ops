CREATE TABLE dim_state_skus (
    state_sku VARCHAR(50) PRIMARY KEY,      -- e.g., 'WYLD-OR-MAR-100', 'WYLD-CA-MAR-100'
    product_id VARCHAR(50),                 -- Foreign key linking to dim_products
    state_code VARCHAR(2),                  -- OR, CA, WA, CO, etc.
    metrc_item_id VARCHAR(100),             -- State compliance system tracking ID/Name
    wholesale_price_case NUMERIC(10,2),     -- Case pricing for dispensary B2B sales
    units_per_case INT,                     -- e.g., 20 boxes per case
    is_active BOOLEAN,                      -- To handle state-specific product retirements
    FOREIGN KEY (product_id) REFERENCES dim_products(product_id)
);