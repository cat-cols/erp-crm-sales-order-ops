-- =============================================================================
-- schema.sql
-- Wyld Sales Operations — SQLite Database Schema
-- =============================================================================
-- Tables:
--   products          SKU catalog
--   sales_reps        Territory representatives
--   customers         Dispensary / retail accounts
--   inventory         Warehouse stock levels
--   state_compliance  Per-market regulatory rules
--   orders            Order headers
--   order_items       Order line items
--
-- Analytical views (business intelligence layer):
--   vw_order_summary          Full order detail joined across all tables
--   vw_revenue_by_market      Revenue, units, order count per market
--   vw_revenue_by_rep         Rep performance: revenue, orders, avg order value
--   vw_product_performance    SKU velocity, revenue, compliance flag rate
--   vw_account_health         Customer-level AR aging + order history
--   vw_compliance_flags       All flagged orders with reason detail
--   vw_inventory_status       Stock levels vs reorder points
--   vw_open_orders            Pending + Processing orders needing action
-- =============================================================================

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- ---------------------------------------------------------------------------
-- Core tables
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS products (
    sku                  TEXT PRIMARY KEY,
    product_name         TEXT NOT NULL,
    format               TEXT NOT NULL CHECK (format IN ('Gummy','Beverage','Mint')),
    flavor               TEXT NOT NULL,
    thc_per_unit_mg      REAL NOT NULL DEFAULT 0,
    cbd_per_unit_mg      REAL NOT NULL DEFAULT 0,
    units_per_pack       INTEGER NOT NULL,
    msrp                 REAL NOT NULL,
    wholesale_price      REAL NOT NULL,
    cost_of_goods        REAL NOT NULL,
    is_active            INTEGER NOT NULL DEFAULT 1,  -- SQLite has no BOOLEAN
    requires_cold_chain  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS sales_reps (
    rep_id     TEXT PRIMARY KEY,
    rep_name   TEXT NOT NULL,
    region     TEXT NOT NULL,
    markets    TEXT NOT NULL,   -- pipe-delimited market codes
    email      TEXT,
    phone      TEXT,
    hire_date  TEXT
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id          TEXT PRIMARY KEY,
    account_name         TEXT NOT NULL,
    customer_type        TEXT NOT NULL,
    tier                 TEXT NOT NULL CHECK (tier IN ('Platinum','Gold','Silver','Bronze')),
    market               TEXT NOT NULL,
    state_province       TEXT NOT NULL,
    is_canada            INTEGER NOT NULL DEFAULT 0,
    city                 TEXT,
    address              TEXT,
    license_number       TEXT,
    license_expiry       TEXT,
    rep_id               TEXT REFERENCES sales_reps(rep_id),
    payment_terms        TEXT,
    min_order_cases      INTEGER,
    credit_limit         REAL,
    on_credit_hold       INTEGER NOT NULL DEFAULT 0,
    account_open_date    TEXT,
    distribution_channel TEXT
);

CREATE TABLE IF NOT EXISTS inventory (
    sku                  TEXT PRIMARY KEY REFERENCES products(sku),
    product_name         TEXT NOT NULL,
    on_hand_units        INTEGER NOT NULL DEFAULT 0,
    allocated_units      INTEGER NOT NULL DEFAULT 0,
    available_units      INTEGER NOT NULL DEFAULT 0,
    reorder_point        INTEGER NOT NULL DEFAULT 0,
    below_reorder        INTEGER NOT NULL DEFAULT 0,
    last_received_date   TEXT,
    warehouse_location   TEXT
);

CREATE TABLE IF NOT EXISTS state_compliance (
    market                    TEXT PRIMARY KEY,
    is_canada                 INTEGER NOT NULL DEFAULT 0,
    thc_per_unit_limit_mg     REAL NOT NULL,
    max_thc_per_package_mg    REAL NOT NULL,
    requires_child_resistant  INTEGER NOT NULL DEFAULT 1,
    requires_opaque_packaging INTEGER NOT NULL DEFAULT 0,
    requires_universal_symbol INTEGER NOT NULL DEFAULT 1,
    max_units_per_order       INTEGER,
    requires_state_stamp      INTEGER NOT NULL DEFAULT 0,
    notes                     TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id              TEXT PRIMARY KEY,
    customer_id           TEXT NOT NULL REFERENCES customers(customer_id),
    account_name          TEXT NOT NULL,
    market                TEXT NOT NULL REFERENCES state_compliance(market),
    state_province        TEXT NOT NULL,
    is_canada             INTEGER NOT NULL DEFAULT 0,
    rep_id                TEXT REFERENCES sales_reps(rep_id),
    order_date            TEXT NOT NULL,
    fulfillment_date      TEXT,
    invoice_date          TEXT,
    status                TEXT NOT NULL CHECK (status IN (
                              'Pending','Processing','Fulfilled',
                              'Invoiced','Rejected','Returned','Refusal')),
    rejection_reason      TEXT,
    po_number             TEXT,
    payment_terms         TEXT,
    distribution_channel  TEXT,
    order_total           REAL NOT NULL DEFAULT 0,
    has_compliance_flag   INTEGER NOT NULL DEFAULT 0,
    notes                 TEXT
);

CREATE TABLE IF NOT EXISTS order_items (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id             TEXT NOT NULL REFERENCES orders(order_id),
    sku                  TEXT NOT NULL REFERENCES products(sku),
    product_name         TEXT NOT NULL,
    format               TEXT NOT NULL,
    qty_cases            INTEGER NOT NULL,
    unit_price           REAL NOT NULL,
    line_total           REAL NOT NULL,
    thc_per_unit_mg      REAL NOT NULL,
    thc_limit_market     REAL NOT NULL,
    thc_compliance_flag  INTEGER NOT NULL DEFAULT 0,
    cold_chain_required  INTEGER NOT NULL DEFAULT 0
);

-- ---------------------------------------------------------------------------
-- Indexes — speed up the queries analysts actually run
-- ---------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_orders_customer    ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_market      ON orders(market);
CREATE INDEX IF NOT EXISTS idx_orders_rep         ON orders(rep_id);
CREATE INDEX IF NOT EXISTS idx_orders_status      ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_date        ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_flag        ON orders(has_compliance_flag);
CREATE INDEX IF NOT EXISTS idx_items_order        ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_items_sku          ON order_items(sku);
CREATE INDEX IF NOT EXISTS idx_items_flag         ON order_items(thc_compliance_flag);
CREATE INDEX IF NOT EXISTS idx_customers_market   ON customers(market);
CREATE INDEX IF NOT EXISTS idx_customers_tier     ON customers(tier);
CREATE INDEX IF NOT EXISTS idx_customers_hold     ON customers(on_credit_hold);

-- ---------------------------------------------------------------------------
-- Analytical views
-- ---------------------------------------------------------------------------

-- Full order detail — the primary working view for the Sales team
CREATE VIEW IF NOT EXISTS vw_order_summary AS
SELECT
    o.order_id,
    o.order_date,
    o.fulfillment_date,
    o.invoice_date,
    o.status,
    o.rejection_reason,
    o.po_number,
    o.payment_terms,
    o.distribution_channel,
    o.order_total,
    o.has_compliance_flag,
    c.customer_id,
    c.account_name,
    c.customer_type,
    c.tier,
    c.market,
    c.is_canada,
    c.city,
    c.license_number,
    c.license_expiry,
    c.on_credit_hold,
    r.rep_name,
    r.region,
    -- Days to fulfill (null if not yet fulfilled)
    CASE
        WHEN o.fulfillment_date IS NOT NULL
        THEN CAST(JULIANDAY(o.fulfillment_date) - JULIANDAY(o.order_date) AS INTEGER)
        ELSE NULL
    END AS days_to_fulfill,
    -- Days to invoice (null if not yet invoiced)
    CASE
        WHEN o.invoice_date IS NOT NULL
        THEN CAST(JULIANDAY(o.invoice_date) - JULIANDAY(o.order_date) AS INTEGER)
        ELSE NULL
    END AS days_to_invoice,
    -- AR aging bucket (from invoice date)
    CASE
        WHEN o.status != 'Invoiced'   THEN 'N/A'
        WHEN o.invoice_date IS NULL   THEN 'N/A'
        WHEN JULIANDAY('now') - JULIANDAY(o.invoice_date) <= 15  THEN 'Current'
        WHEN JULIANDAY('now') - JULIANDAY(o.invoice_date) <= 30  THEN '16-30 days'
        WHEN JULIANDAY('now') - JULIANDAY(o.invoice_date) <= 45  THEN '31-45 days'
        WHEN JULIANDAY('now') - JULIANDAY(o.invoice_date) <= 60  THEN '46-60 days'
        ELSE '60+ days'
    END AS ar_aging_bucket
FROM orders o
JOIN customers c  ON o.customer_id = c.customer_id
JOIN sales_reps r ON o.rep_id = r.rep_id;

-- Revenue by market — used in dashboard choropleth
CREATE VIEW IF NOT EXISTS vw_revenue_by_market AS
SELECT
    market,
    is_canada,
    COUNT(*)                                         AS total_orders,
    SUM(CASE WHEN status = 'Invoiced'  THEN 1 ELSE 0 END) AS invoiced_orders,
    SUM(CASE WHEN status = 'Rejected'  THEN 1 ELSE 0 END) AS rejected_orders,
    SUM(CASE WHEN status = 'Returned'  THEN 1 ELSE 0 END) AS returned_orders,
    ROUND(SUM(CASE WHEN status IN ('Invoiced','Fulfilled')
              THEN order_total ELSE 0 END), 2)       AS total_revenue,
    ROUND(AVG(CASE WHEN status IN ('Invoiced','Fulfilled')
              THEN order_total END), 2)              AS avg_order_value,
    ROUND(
        100.0 * SUM(CASE WHEN status = 'Invoiced' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 1
    )                                                AS invoice_rate_pct,
    ROUND(
        100.0 * SUM(CASE WHEN status = 'Rejected' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 1
    )                                                AS rejection_rate_pct
FROM orders
GROUP BY market, is_canada;

-- Rep performance dashboard
CREATE VIEW IF NOT EXISTS vw_revenue_by_rep AS
SELECT
    r.rep_id,
    r.rep_name,
    r.region,
    COUNT(o.order_id)                                   AS total_orders,
    SUM(CASE WHEN o.status = 'Invoiced'  THEN 1 ELSE 0 END) AS invoiced_orders,
    SUM(CASE WHEN o.status = 'Rejected'  THEN 1 ELSE 0 END) AS rejected_orders,
    ROUND(SUM(CASE WHEN o.status IN ('Invoiced','Fulfilled')
              THEN o.order_total ELSE 0 END), 2)         AS total_revenue,
    ROUND(AVG(CASE WHEN o.status IN ('Invoiced','Fulfilled')
              THEN o.order_total END), 2)                AS avg_order_value,
    COUNT(DISTINCT o.customer_id)                       AS unique_accounts,
    ROUND(
        100.0 * SUM(CASE WHEN o.status = 'Invoiced' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(o.order_id), 0), 1
    )                                                   AS invoice_rate_pct
FROM sales_reps r
LEFT JOIN orders o ON r.rep_id = o.rep_id
GROUP BY r.rep_id, r.rep_name, r.region;

-- SKU performance — velocity, revenue, compliance flag rate
CREATE VIEW IF NOT EXISTS vw_product_performance AS
SELECT
    i.sku,
    i.product_name,
    i.format,
    COUNT(DISTINCT oi.order_id)                          AS orders_containing_sku,
    SUM(oi.qty_cases)                                    AS total_cases_sold,
    ROUND(SUM(oi.line_total), 2)                         AS total_revenue,
    ROUND(AVG(oi.unit_price), 2)                         AS avg_unit_price,
    SUM(CASE WHEN oi.thc_compliance_flag = 1 THEN 1 ELSE 0 END) AS compliance_flag_count,
    ROUND(
        100.0 * SUM(CASE WHEN oi.thc_compliance_flag = 1 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 1
    )                                                    AS flag_rate_pct,
    inv.on_hand_units,
    inv.available_units,
    inv.below_reorder,
    inv.warehouse_location
FROM order_items oi
JOIN products i   ON oi.sku = i.sku
JOIN inventory inv ON oi.sku = inv.sku
GROUP BY i.sku, i.product_name, i.format;

-- Account health — AR aging + lifetime value + hold status
CREATE VIEW IF NOT EXISTS vw_account_health AS
SELECT
    c.customer_id,
    c.account_name,
    c.tier,
    c.market,
    c.customer_type,
    c.payment_terms,
    c.credit_limit,
    c.on_credit_hold,
    c.license_expiry,
    COUNT(o.order_id)                                       AS lifetime_orders,
    ROUND(SUM(CASE WHEN o.status IN ('Invoiced','Fulfilled')
              THEN o.order_total ELSE 0 END), 2)           AS lifetime_revenue,
    ROUND(AVG(CASE WHEN o.status IN ('Invoiced','Fulfilled')
              THEN o.order_total END), 2)                  AS avg_order_value,
    MAX(o.order_date)                                       AS last_order_date,
    SUM(CASE WHEN o.status = 'Rejected' THEN 1 ELSE 0 END) AS rejected_orders,
    SUM(CASE WHEN o.status = 'Returned' THEN 1 ELSE 0 END) AS returned_orders,
    -- Open AR (invoiced but not yet collected — simplified)
    ROUND(SUM(CASE WHEN o.status = 'Invoiced'
              AND JULIANDAY('now') - JULIANDAY(o.invoice_date) > 0
              THEN o.order_total ELSE 0 END), 2)           AS open_ar_amount,
    -- Flag if license expires within 60 days
    CASE
        WHEN JULIANDAY(c.license_expiry) - JULIANDAY('now') < 0  THEN 'EXPIRED'
        WHEN JULIANDAY(c.license_expiry) - JULIANDAY('now') < 60 THEN 'EXPIRING SOON'
        ELSE 'Valid'
    END AS license_status
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.account_name, c.tier, c.market,
         c.customer_type, c.payment_terms, c.credit_limit,
         c.on_credit_hold, c.license_expiry;

-- Compliance flags — QC review queue
CREATE VIEW IF NOT EXISTS vw_compliance_flags AS
SELECT
    o.order_id,
    o.order_date,
    o.status,
    o.market,
    c.account_name,
    c.tier,
    c.license_number,
    c.license_expiry,
    r.rep_name,
    oi.sku,
    oi.product_name,
    oi.thc_per_unit_mg,
    oi.thc_limit_market,
    oi.thc_per_unit_mg - oi.thc_limit_market AS thc_overage_mg,
    oi.qty_cases,
    oi.line_total,
    sc.requires_opaque_packaging,
    sc.requires_state_stamp,
    sc.notes AS market_notes
FROM order_items oi
JOIN orders o           ON oi.order_id = o.order_id
JOIN customers c        ON o.customer_id = c.customer_id
JOIN sales_reps r       ON o.rep_id = r.rep_id
JOIN state_compliance sc ON o.market = sc.market
WHERE oi.thc_compliance_flag = 1
ORDER BY o.order_date DESC;

-- Inventory status with reorder alerts
CREATE VIEW IF NOT EXISTS vw_inventory_status AS
SELECT
    inv.sku,
    inv.product_name,
    inv.warehouse_location,
    inv.on_hand_units,
    inv.allocated_units,
    inv.available_units,
    inv.reorder_point,
    inv.below_reorder,
    inv.last_received_date,
    p.format,
    p.wholesale_price,
    ROUND(inv.available_units * p.wholesale_price, 2) AS inventory_value,
    CASE
        WHEN inv.available_units = 0          THEN 'OUT OF STOCK'
        WHEN inv.below_reorder = 1            THEN 'REORDER NOW'
        WHEN inv.available_units < inv.reorder_point * 1.25 THEN 'LOW STOCK'
        ELSE 'OK'
    END AS stock_status
FROM inventory inv
JOIN products p ON inv.sku = p.sku;

-- Open orders needing action (Pending or Processing)
CREATE VIEW IF NOT EXISTS vw_open_orders AS
SELECT
    o.order_id,
    o.order_date,
    o.status,
    o.market,
    o.order_total,
    o.po_number,
    o.distribution_channel,
    o.has_compliance_flag,
    c.account_name,
    c.tier,
    c.on_credit_hold,
    r.rep_name,
    CAST(JULIANDAY('now') - JULIANDAY(o.order_date) AS INTEGER) AS days_open
FROM orders o
JOIN customers c  ON o.customer_id = c.customer_id
JOIN sales_reps r ON o.rep_id = r.rep_id
WHERE o.status IN ('Pending', 'Processing')
ORDER BY o.order_date ASC;