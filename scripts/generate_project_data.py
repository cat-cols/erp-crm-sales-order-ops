"""
generate_data.py
================
Myld Sales Operations — Mock Data Generator

Generates a realistic, relational dataset simulating Myld's B2B sales
operations across all 16 US states + Canada. Outputs CSVs consumed by
every downstream module (database, pipeline, reporting, dashboard).

Tables produced:
    products.csv        — SKU catalog with THC/CBD content, format, price tiers
    customers.csv       — Dispensary accounts with tier, state, license info
    sales_reps.csv      — Territory reps mapped to states
    orders.csv          — Order headers (1 row per order)
    order_items.csv     — Line items (N rows per order)
    inventory.csv       — Current warehouse stock levels per SKU
    state_compliance.csv— Per-state THC limits, packaging rules, flags

Usage:
    python generate_data.py              # default: ~1,200 orders
    python generate_data.py --orders 500 # custom volume
"""

import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker("en_US")
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# ---------------------------------------------------------------------------
# Constants — mirroring Myld's real footprint
# ---------------------------------------------------------------------------

MYLD_USA = [
    "AZ", "CA", "CO", "IL", "MA", "MD", "MI", "MO",
    "NJ", "NM", "NV", "NY", "OH", "OR", "OK", "WA"
]

MYLD_CANADA = ["AB", "BC", "MB", "NB", "NL", "NS", "ON", "PE", "QC", "SK"]

ALL_MARKETS = MYLD_USA + MYLD_CANADA

# Market tier classification for realistic distribution weights
PRIMARY_MARKETS = ["OR", "WA", "CA", "CO"]
SECONDARY_MARKETS = ["AZ", "NV", "IL", "MI", "MA", "NY", "NJ", "OH", "OK", "MD", "MO", "NM"]
CANADA_MARKETS = ["AB", "BC", "ON", "QC"]
OTHER_CANADA = ["MB", "NB", "NL", "NS", "PE", "SK"]

# State-level THC per-unit limits (mg) — simplified from real regs
STATE_THC_LIMITS = {
    "AZ": 10, "CA": 10, "CO": 10, "IL": 5,  "MA": 5,  "MD": 10,
    "MI": 10, "MO": 10, "NJ": 5,  "NM": 10, "NV": 10, "NY": 5,
    "OH": 10, "OR": 10, "OK": 10, "WA": 10,
    # Canada — federal limit 10mg/unit
    "AB": 10, "BC": 10, "MB": 10, "NB": 10, "NL": 10,
    "NS": 10, "ON": 10, "PE": 10, "QC": 10, "SK": 10,
}

# Myld's actual product lines
MYLD_PRODUCTS: list[dict[str, Any]] = [
    {"sku": "SKU0001", "product_name": "Myld Orange 1:1 THC:CBC Gummies", "flavor": "Orange", "base_price": 10.00, "cogs_ratio": 0.45, "msrp": 22.00, "thc_per_unit_mg": 10, "cbd_per_unit_mg": 0, "units_per_pack": 20},
    {"sku": "SKU0002", "product_name": "Myld Elderberry 1:1:1 THC:CBD:CBN Gummies", "flavor": "Elderberry", "base_price": 10.00, "cogs_ratio": 0.47, "msrp": 22.00, "thc_per_unit_mg": 10, "cbd_per_unit_mg": 10, "units_per_pack": 20},
    {"sku": "SKU0003", "product_name": "Myld Moonberry 2:1 THC:CBN Gummies", "flavor": "Moonberry", "base_price": 10.50, "cogs_ratio": 0.46, "msrp": 25.00, "thc_per_unit_mg": 10, "cbd_per_unit_mg": 0, "units_per_pack": 20},
    {"sku": "SKU0004", "product_name": "Myld Watermelon 1:1:1 THC:CBG:CBC Gummies", "flavor": "Watermelon", "base_price": 10.50, "cogs_ratio": 0.48, "msrp": 22.00, "thc_per_unit_mg": 10, "cbd_per_unit_mg": 0, "units_per_pack": 20},
    {"sku": "SKU0005", "product_name": "Myld Salmonberry THC Gummies", "flavor": "Salmonberry", "base_price": 10.00, "cogs_ratio": 0.42, "msrp": 22.00, "thc_per_unit_mg": 10, "cbd_per_unit_mg": 0, "units_per_pack": 20},
    {"sku": "SKU0006", "product_name": "Myld Mangosteen 1:1 THC:THCv Gummies", "flavor": "Mangosteen", "base_price": 10.50, "cogs_ratio": 0.49, "msrp": 22.00, "thc_per_unit_mg": 10, "cbd_per_unit_mg": 0, "units_per_pack": 20},
    {"sku": "SKU0007", "product_name": "Myld Acai THC Gummies", "flavor": "Acai", "base_price": 10.00, "cogs_ratio": 0.42, "msrp": 22.00, "thc_per_unit_mg": 10, "cbd_per_unit_mg": 0, "units_per_pack": 20},
    {"sku": "SKU0008", "product_name": "Myld Peach 2:1 CBD:THC Gummies", "flavor": "Peach", "base_price": 10.50, "cogs_ratio": 0.46, "msrp": 22.00, "thc_per_unit_mg": 10, "cbd_per_unit_mg": 20, "units_per_pack": 20},
    {"sku": "SKU0009", "product_name": "Myld Jabuticaba 1:1 THC:CBG Gummies", "flavor": "Jabuticaba", "base_price": 10.50, "cogs_ratio": 0.47, "msrp": 22.00, "thc_per_unit_mg": 10, "cbd_per_unit_mg": 0, "units_per_pack": 20},
    {"sku": "SKU0010", "product_name": "Myld Grape 1:1 THC:CBD Gummies", "flavor": "Grape", "base_price": 10.50, "cogs_ratio": 0.46, "msrp": 22.00, "thc_per_unit_mg": 10, "cbd_per_unit_mg": 10, "units_per_pack": 20},
    {"sku": "SKU0011", "product_name": "Myld Cloudberry THC Gummies", "flavor": "Cloudberry", "base_price": 10.50, "cogs_ratio": 0.42, "msrp": 22.00, "thc_per_unit_mg": 10, "cbd_per_unit_mg": 0, "units_per_pack": 20},
    {"sku": "SKU0012", "product_name": "Myld Sour Banana THC Gummies", "flavor": "Sour Banana", "base_price": 10.50, "cogs_ratio": 0.42, "msrp": 22.00, "thc_per_unit_mg": 10, "cbd_per_unit_mg": 0, "units_per_pack": 20},
    {"sku": "SKU0013", "product_name": "Myld Sour Grapefruit THC Gummies", "flavor": "Sour Grapefruit", "base_price": 10.50, "cogs_ratio": 0.42, "msrp": 22.00, "thc_per_unit_mg": 10, "cbd_per_unit_mg": 0, "units_per_pack": 20},
    {"sku": "SKU0014", "product_name": "Myld Sour Lemon THC Gummies", "flavor": "Sour Lemon", "base_price": 10.50, "cogs_ratio": 0.43, "msrp": 22.00, "thc_per_unit_mg": 10, "cbd_per_unit_mg": 0, "units_per_pack": 20},
    {"sku": "SKU0015", "product_name": "Myld Pineapple 20:1 CBD:THC Gummies", "flavor": "Pineapple", "base_price": 10.50, "cogs_ratio": 0.47, "msrp": 19.00, "thc_per_unit_mg": 10, "cbd_per_unit_mg": 200, "units_per_pack": 20},
]

# Customer tiering
CUSTOMER_TIERS = ["Platinum", "Gold", "Silver", "Bronze"]
TIER_WEIGHTS = [0.10, 0.20, 0.40, 0.30]

CUSTOMER_TYPES = ["Dispensary", "Retail Chain", "Delivery Service", "Wholesale"]

# Order lifecycle
ORDER_STATUSES = [
    "Pending", "Processing", "Fulfilled", "Invoiced",
    "Rejected", "Returned", "Refusal"
]

REJECTION_REASONS = [
    "Exceeds state THC limit",
    "License expired",
    "Packaging non-compliant",
    "Minimum order not met",
    "Account on credit hold",
    "Duplicate order",
]

PAYMENT_TERMS = ["Net 15", "Net 30", "Net 45", "COD", "Prepaid"]

DISTRIBUTION_CHANNELS = ["Direct", "Third-Party Distributor", "Platform"]

OUTPUT_DIR = Path("data")

# Date boundaries
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 3, 31)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sku_code(idx: int) -> str:
    """Generate sequential SKU codes."""
    return f"MLD-{idx+1:04d}"


def date_range_days(start: datetime, end: datetime) -> int:
    """Calculate days between two dates."""
    return (end - start).days


def random_date(start: datetime, end: datetime) -> datetime:
    """Generate a random date within a range."""
    return start + timedelta(days=random.randint(0, date_range_days(start, end)))


def get_market_weight(market: str) -> int:
    """Return distribution weight for a given market."""
    if market in PRIMARY_MARKETS:
        weights = {"OR": 12, "WA": 12, "CA": 15, "CO": 10}
        return weights.get(market, 10)
    elif market in CANADA_MARKETS:
        weights = {"ON": 8, "BC": 7, "AB": 5, "QC": 4}
        return weights.get(market, 4)
    elif market in SECONDARY_MARKETS:
        weights = {"NV": 6, "MI": 5, "IL": 5, "MA": 5, "NY": 4, "NJ": 3, "OH": 3, "OK": 3, "MD": 2, "MO": 2, "NM": 2}
        return weights.get(market, 3)
    else:
        return 2


def build_market_probs() -> list[float]:
    """Build probability distribution for market selection."""
    weights = [get_market_weight(m) for m in ALL_MARKETS]
    total = sum(weights)
    return [w / total for w in weights]


# ---------------------------------------------------------------------------
# Generator functions
# ---------------------------------------------------------------------------

def generate_products() -> pd.DataFrame:
    """Build the SKU catalog with wholesale pricing based on market-specific adjustments."""
    rows = []

    # Market price modifiers based on real regional differences
    market_price_modifier = {
        "OR": 1.00,  # Oregon - base pricing
        "WA": 1.05,
        "CA": 1.15,  # California - typically more expensive
        "CO": 1.05,
        # Default for other markets
        "default": 1.08
    }

    for idx, product in enumerate(MYLD_PRODUCTS):
        # Base wholesale price (per unit in a case of 10)
        base_wholesale = round(product["base_price"] * 10, 2)
        cost_of_goods = round(product["base_price"] * 10 * product["cogs_ratio"], 2)

        # Generate market-specific pricing for major markets
        for market in PRIMARY_MARKETS:
            modifier = market_price_modifier.get(market, market_price_modifier["default"])
            wholesale_case_price = round(base_wholesale * modifier, 2)
            market_cogs = round(cost_of_goods * modifier, 2)

            rows.append({
                "state_sku": f"{market}-{product['sku']}",
                "global_sku": sku_code(idx),
                "market": market,
                "product_name": product["product_name"],
                "format": "Gummy",
                "flavor": product["flavor"],
                "thc_per_unit_mg": product["thc_per_unit_mg"],
                "cbd_per_unit_mg": product["cbd_per_unit_mg"],
                "units_per_pack": product["units_per_pack"],
                "msrp": product["msrp"],
                "wholesale_case_price": wholesale_case_price,
                "cost_of_goods": market_cogs,
                "is_active": True,
                "requires_cold_chain": False,
                "metrc_item_name": f"{market}_Myld_{product['product_name'].replace(' ', '_').replace(':', '_')}",
            })

        # Add a default entry for non-primary markets
        default_modifier = market_price_modifier["default"]
        rows.append({
            "state_sku": f"DEFAULT-{product['sku']}",
            "global_sku": sku_code(idx),
            "market": "DEFAULT",
            "product_name": product["product_name"],
            "format": "Gummy",
            "flavor": product["flavor"],
            "thc_per_unit_mg": product["thc_per_unit_mg"],
            "cbd_per_unit_mg": product["cbd_per_unit_mg"],
            "units_per_pack": product["units_per_pack"],
            "msrp": product["msrp"],
            "wholesale_case_price": round(base_wholesale * default_modifier, 2),
            "cost_of_goods": round(cost_of_goods * default_modifier, 2),
            "is_active": True,
            "requires_cold_chain": False,
            "metrc_item_name": f"GEN_Myld_{product['product_name'].replace(' ', '_').replace(':', '_')}",
        })

    df = pd.DataFrame(rows)
    print(f"  [products]   {len(df)} SKU-market combinations generated")
    return df


def generate_sales_reps() -> pd.DataFrame:
    """Create territory reps, each covering specific markets."""
    territories = [
        ("West Coast",     ["CA", "OR", "WA", "NV"]),
        ("Mountain",       ["CO", "AZ", "NM", "OK"]),
        ("Midwest",        ["IL", "MI", "OH", "MO"]),
        ("Northeast",      ["NY", "NJ", "MA", "MD"]),
        ("Canada West",    ["BC", "AB", "SK", "MB"]),
        ("Canada East",    ["ON", "QC", "NS", "NB", "NL", "PE"]),
    ]

    rows = []
    for rep_id, (region, markets) in enumerate(territories, start=1):
        hire_date = fake.date_between(start_date="-5y", end_date="-6m")
        rows.append({
            "rep_id": f"REP-{rep_id:03d}",
            "rep_name": fake.name(),
            "region": region,
            "markets": "|".join(markets),
            "email": fake.company_email(),
            "phone": fake.phone_number(),
            "hire_date": hire_date,
        })

    df = pd.DataFrame(rows)
    print(f"  [sales_reps] {len(df)} reps generated")
    return df


def build_rep_lookup(reps_df: pd.DataFrame) -> dict[str, str]:
    """Build a market-to-rep lookup dictionary for fast assignment."""
    lookup = {}
    for _, rep in reps_df.iterrows():
        for market in rep["markets"].split("|"):
            lookup[market] = rep["rep_id"]
    return lookup


def generate_customers(reps_df: pd.DataFrame, n: int = 180) -> pd.DataFrame:
    """
    Create dispensary/retail accounts distributed across all markets.
    Heavier weight on primary markets reflecting Myld's strongest presence.
    """
    market_probs = build_market_probs()
    rep_lookup = build_rep_lookup(reps_df)

    rows = []
    for cust_id in range(1, n + 1):
        market = np.random.choice(ALL_MARKETS, p=market_probs)
        is_canada = market in MYLD_CANADA
        tier = random.choices(CUSTOMER_TIERS, weights=TIER_WEIGHTS)[0]

        # Tier-based business rules
        tier_config = {
            "Platinum": {"min_order": 20, "credit_limit": 50000, "terms": ["Net 30", "Net 45"]},
            "Gold": {"min_order": 12, "credit_limit": 25000, "terms": ["Net 30", "Net 45"]},
            "Silver": {"min_order": 6, "credit_limit": 10000, "terms": ["Net 15", "Net 30"]},
            "Bronze": {"min_order": 3, "credit_limit": 5000, "terms": ["Net 15", "Net 30", "COD"]},
        }

        config = tier_config[tier]

        # Account name generation with market context
        if is_canada:
            company_suffix = " Cannabis Co."
        else:
            company_suffix = " Cannabis" if random.random() < 0.7 else " Dispensary"

        # Credit hold logic - higher tiers are less likely to be on hold
        credit_hold_prob = {
            "Platinum": 0.01,
            "Gold": 0.02,
            "Silver": 0.04,
            "Bronze": 0.08,
        }

        # Assign rep, with fallback for unassigned markets
        rep_id = rep_lookup.get(market)
        if not rep_id:
            rep_id = reps_df.sample(1)["rep_id"].values[0]

        rows.append({
            "customer_id": f"CUST-{cust_id:04d}",
            "account_name": fake.company() + company_suffix,
            "customer_type": random.choices(
                CUSTOMER_TYPES,
                weights=[0.65, 0.15, 0.15, 0.05]
            )[0],
            "tier": tier,
            "market": market,
            "state_province": market,
            "is_canada": is_canada,
            "city": fake.city(),
            "address": fake.street_address(),
            "license_number": f"{'MED' if not is_canada else 'HC'}-{fake.bothify('??####??').upper()}",
            "license_expiry": fake.date_between(start_date="today", end_date="+2y"),
            "rep_id": rep_id,
            "payment_terms": random.choice(config["terms"]),
            "min_order_cases": config["min_order"],
            "credit_limit": config["credit_limit"],
            "on_credit_hold": random.random() < credit_hold_prob[tier],
            "account_open_date": fake.date_between(start_date="-4y", end_date="-3m"),
            "distribution_channel": random.choices(
                DISTRIBUTION_CHANNELS,
                weights=[0.50, 0.35, 0.15]
            )[0],
        })

    df = pd.DataFrame(rows)
    print(f"  [customers]  {len(df)} accounts generated across {df['market'].nunique()} markets")
    return df


def generate_inventory(products_df: pd.DataFrame) -> pd.DataFrame:
    """Current warehouse stock levels per SKU."""
    rows = []

    # Get unique global SKUs for inventory (not market-specific)
    unique_skus = products_df[products_df["market"] == "DEFAULT"][["global_sku", "product_name"]].drop_duplicates()

    for _, prod in unique_skus.iterrows():
        on_hand = random.randint(50, 2000)
        allocated = random.randint(0, min(on_hand, 500))
        available = on_hand - allocated
        reorder = random.randint(100, 300)

        rows.append({
            "sku": prod["global_sku"],
            "product_name": prod["product_name"],
            "on_hand_units": on_hand,
            "allocated_units": allocated,
            "available_units": available,
            "reorder_point": reorder,
            "below_reorder": available < reorder,
            "last_received_date": fake.date_between(start_date="-60d", end_date="today"),
            "warehouse_location": random.choice(["PDX-A", "PDX-B", "DEN-A", "CHI-A"]),
        })

    df = pd.DataFrame(rows)
    print(f"  [inventory]  {len(df)} SKU inventory records generated")
    return df


def generate_state_compliance() -> pd.DataFrame:
    """Per-market compliance rules used by the QC checker."""
    rows = []

    market_configs = {
        "recreational_medical": ["CA", "CO", "OR", "WA", "NV"],
        "medical_only": ["OK", "MO", "MD"],
        "opaque_packaging": ["IL", "MA", "NJ", "NY", "QC"],
        "state_stamp": ["CA", "CO", "IL", "WA"],
    }

    for market in ALL_MARKETS:
        is_canada = market in MYLD_CANADA
        thc_limit = STATE_THC_LIMITS.get(market, 10)

        # Determine market type
        if market in market_configs["recreational_medical"]:
            market_type = "Recreational + medical"
        elif market in market_configs["medical_only"]:
            market_type = "Medical only"
        elif is_canada:
            market_type = "Federal framework"
        else:
            market_type = "Adult use"

        rows.append({
            "market": market,
            "is_canada": is_canada,
            "thc_per_unit_limit_mg": thc_limit,
            "max_thc_per_package_mg": 100 if thc_limit == 10 else 50,
            "requires_child_resistant": True,
            "requires_opaque_packaging": market in market_configs["opaque_packaging"],
            "requires_universal_symbol": not is_canada,
            "max_units_per_order": random.choice([500, 1000, 2000, None]),
            "requires_state_stamp": market in market_configs["state_stamp"],
            "notes": market_type,
        })

    df = pd.DataFrame(rows)
    print(f"  [compliance] {len(df)} market compliance records generated")
    return df


def generate_orders(
    products_df: pd.DataFrame,
    customers_df: pd.DataFrame,
    compliance_df: pd.DataFrame,
    n_orders: int = 1200,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate order headers + line items.

    Realistic order lifecycle logic:
    - ~78% of orders reach Invoiced/Fulfilled
    - ~8% Rejected (license, THC limit, credit hold, minimum not met)
    - ~5% Returned
    - ~4% Refusal (delivery refused at door)
    - ~5% still Pending/Processing (recent orders in flight)
    """
    # Build lookup dictionaries for performance
    compliance_map = compliance_df.set_index("market").to_dict("index")

    # Get default product pricing (for non-primary markets)
    default_products = products_df[products_df["market"] == "DEFAULT"].set_index("global_sku")

    # Build market-specific product lookup
    market_products = {}
    for market in PRIMARY_MARKETS:
        market_df = products_df[products_df["market"] == market].set_index("global_sku")
        if not market_df.empty:
            market_products[market] = market_df

    # Status distribution based on order age
    def determine_status(order_date: datetime, customer_on_hold: bool) -> tuple[str, str | None]:
        days_old = (END_DATE - order_date).days

        if days_old < 7:
            return random.choices(
                ["Pending", "Processing"],
                weights=[0.6, 0.4]
            )[0], None

        if customer_on_hold and random.random() < 0.7:
            return "Rejected", "Account on credit hold"

        status = random.choices(
            ["Invoiced", "Fulfilled", "Rejected", "Returned", "Refusal", "Pending", "Processing"],
            weights=[0.60, 0.18, 0.08, 0.05, 0.04, 0.03, 0.02]
        )[0]

        rejection_reason = None
        if status == "Rejected":
            rejection_reason = random.choice(REJECTION_REASONS[:-1])  # Exclude None

        return status, rejection_reason

    order_rows = []
    item_rows = []

    for order_num in range(1, n_orders + 1):
        cust = customers_df.sample(1).iloc[0]
        market = cust["market"]
        comp = compliance_map[market]
        order_date = random_date(START_DATE, END_DATE)

        # Determine order status
        status, rejection_reason = determine_status(order_date, cust["on_credit_hold"])

        # Fulfillment and invoice dates
        fulfillment_date = None
        invoice_date = None
        if status in ("Fulfilled", "Invoiced"):
            fulfillment_date = order_date + timedelta(days=random.randint(1, 5))
        if status == "Invoiced":
            invoice_date = fulfillment_date + timedelta(days=random.randint(0, 2))

        # Get appropriate product pricing for this market
        if market in market_products:
            product_pricing = market_products[market]
        else:
            product_pricing = default_products

        # PO number (some accounts use them, some don't)
        po_number = f"PO-{fake.bothify('####??').upper()}" if random.random() < 0.65 else None

        order_id = f"ORD-{order_num:05d}"

        # Generate line items
        n_lines = random.randint(1, 6)
        available_skus = product_pricing.index.tolist()
        skus_chosen = random.sample(available_skus, min(n_lines, len(available_skus)))

        order_total = 0.0
        has_compliance_flag = False

        for sku in skus_chosen:
            prod = product_pricing.loc[sku]
            qty_cases = random.randint(1, 20)
            unit_price = prod["wholesale_case_price"]

            # Volume discount for high-tier customers
            if cust["tier"] == "Platinum" and qty_cases >= 10:
                unit_price = round(unit_price * 0.92, 2)
            elif cust["tier"] == "Gold" and qty_cases >= 10:
                unit_price = round(unit_price * 0.95, 2)

            line_total = round(qty_cases * unit_price, 2)
            order_total += line_total

            # THC compliance check
            thc_flag = prod["thc_per_unit_mg"] > comp["thc_per_unit_limit_mg"]
            if thc_flag:
                has_compliance_flag = True

            item_rows.append({
                "order_id": order_id,
                "sku": sku,
                "product_name": prod["product_name"],
                "format": prod["format"],
                "qty_cases": qty_cases,
                "unit_price": unit_price,
                "line_total": line_total,
                "thc_per_unit_mg": prod["thc_per_unit_mg"],
                "thc_limit_market": comp["thc_per_unit_limit_mg"],
                "thc_compliance_flag": thc_flag,
                "cold_chain_required": prod["requires_cold_chain"],
            })

        order_rows.append({
            "order_id": order_id,
            "customer_id": cust["customer_id"],
            "account_name": cust["account_name"],
            "market": market,
            "state_province": market,
            "is_canada": cust["is_canada"],
            "rep_id": cust["rep_id"],
            "order_date": order_date.date(),
            "fulfillment_date": fulfillment_date.date() if fulfillment_date else None,
            "invoice_date": invoice_date.date() if invoice_date else None,
            "status": status,
            "rejection_reason": rejection_reason,
            "po_number": po_number,
            "payment_terms": cust["payment_terms"],
            "distribution_channel": cust["distribution_channel"],
            "order_total": round(order_total, 2),
            "has_compliance_flag": has_compliance_flag,
            "notes": None,
        })

    orders_df = pd.DataFrame(order_rows)
    items_df = pd.DataFrame(item_rows)

    print(f"  [orders]     {len(orders_df)} orders generated")
    print(f"  [order_items]{len(items_df)} line items generated")
    _print_order_status_summary(orders_df)
    return orders_df, items_df


def _print_order_status_summary(orders_df: pd.DataFrame) -> None:
    """Print summary of order statuses."""
    summary = orders_df["status"].value_counts()
    for status, count in summary.items():
        pct = count / len(orders_df) * 100
        print(f"               {status:<12} {count:>4}  ({pct:.1f}%)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(n_orders: int = 1200) -> None:
    """Generate all datasets and write to CSV."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    print("\n Myld Sales Ops — Data Generator")
    print("=" * 42)

    # Generate datasets in dependency order
    products_df = generate_products()
    reps_df = generate_sales_reps()
    customers_df = generate_customers(reps_df)
    inventory_df = generate_inventory(products_df)
    compliance_df = generate_state_compliance()
    orders_df, items_df = generate_orders(
        products_df, customers_df, compliance_df, n_orders=n_orders
    )

    # Write all CSVs
    files = {
        "products.csv": products_df,
        "sales_reps.csv": reps_df,
        "customers.csv": customers_df,
        "inventory.csv": inventory_df,
        "state_compliance.csv": compliance_df,
        "orders.csv": orders_df,
        "order_items.csv": items_df,
    }

    for fname, df in files.items():
        path = OUTPUT_DIR / fname
        df.to_csv(path, index=False)
        print(f"  Saved → {path}")

    print(f"\n Done. {len(files)} CSV files written to ./{OUTPUT_DIR}/")
    print(f"  Orders: {n_orders}  |  Line items: {len(items_df)}")
    print(f"  Markets: {orders_df['market'].nunique()} of {len(ALL_MARKETS)} active")
    print(f"  Date range: {START_DATE.date()} → {END_DATE.date()}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Myld mock data generator")
    parser.add_argument(
        "--orders",
        type=int,
        default=1200,
        help="Number of orders to generate (default: 1200)"
    )
    args = parser.parse_args()
    main(n_orders=args.orders)