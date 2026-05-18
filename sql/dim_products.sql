CREATE TABLE dim_products (
    product_id VARCHAR(50) PRIMARY KEY,     -- Internal global identifier
    product_name VARCHAR(100),              -- e.g., 'Marionberry Indica Gummies'
    product_type VARCHAR(50),              -- Gummy, Beverage, Chocolate
    flavor VARCHAR(50),                    -- Marionberry, Huckleberry, Elderberry, etc.
    terpene_profile VARCHAR(50),           -- Indica, Sativa, Hybrid, Enhanced
    thc_mg_per_gummy NUMERIC(5,2),         -- Cannabinoid dosing per piece
    cbd_mg_per_gummy NUMERIC(5,2),
    cbn_mg_per_gummy NUMERIC(5,2),
    cbg_mg_per_gummy NUMERIC(5,2),
    pieces_per_package INT                 -- Standard is usually 10
);