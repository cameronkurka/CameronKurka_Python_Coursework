import polars as pl
import os
import sys

df = None           
cleaned_df = None   

# Helper functions
def print_separator():
    print("-" * 50)

def print_header(title):
    print()
    print_separator()
    print(title)
    print_separator()

def require_data():
# Check that data has been loaded before running any operation
    if df is None:
        print("ERROR: No data loaded. Please choose option 1 first.")
        return False
    return True


# 1. Load Data
def load_data():
    global df, cleaned_df

    print_header("1. Load Data")

    path = input("Enter CSV file path: ").strip()

    if not os.path.exists(path):
        print(f"ERROR: '{path}' not found. Please check the file path and try again.")
        return

    try:
        df = pl.read_csv(path, infer_schema_length=0)
        cleaned_df = None
        print(f"Loaded '{path}': {df.shape[0]} rows, {df.shape[1]} columns")
    except Exception as e:
        print(f"ERROR: Could not load file. {e}")


# 2. Inspect Data
def inspect_data():
    if not require_data():
        return

    print_header("2. Inspect Data")

    frame = cleaned_df if cleaned_df is not None else df

    print(f"Rows: {frame.shape[0]}   Columns: {frame.shape[1]}")
    print(f"Column names: {', '.join(frame.columns)}")

    print("\nColumn data types:")
    for col, dtype in zip(frame.columns, frame.dtypes):
        print(f"  {col:<22} {str(dtype)}")

    print("\nNull (missing) value counts:")
    null_counts = frame.select(pl.all().is_null().sum())
    for col in frame.columns:
        count = null_counts[col][0]
        note = "  <- has missing values" if count > 0 else ""
        print(f"  {col:<22} {count}{note}")

    print("\nFirst 5 rows:")
    print(frame.head(5))


# 3. Clean Null Values
def clean_null_values():
    global df, cleaned_df

    if not require_data():
        return

    print_header("3. Clean Null Values")

    frame = (cleaned_df if cleaned_df is not None else df).clone()
    original_rows = frame.shape[0]

    # Drop rows where key columns are missing
    critical_cols = ["order_id", "sale_date", "unit_price"]
    existing = [c for c in critical_cols if c in frame.columns]
    frame = frame.drop_nulls(subset=existing)
    dropped = original_rows - frame.shape[0]

    # Fill in missing values for non critical columns
    fill_map = {}
    if "customer_name"    in frame.columns: fill_map["customer_name"]    = "Unknown"
    if "region"           in frame.columns: fill_map["region"]           = "Unknown"
    if "product_category" in frame.columns: fill_map["product_category"] = "Uncategorized"
    if "product_name"     in frame.columns: fill_map["product_name"]     = "Unnamed Product"
    if "quantity"         in frame.columns: fill_map["quantity"]         = "1"

    if fill_map:
        frame = frame.with_columns([
            pl.col(col).fill_null(pl.lit(str(val)))
            for col, val in fill_map.items()
        ])

    cleaned_df = frame

    print(f"Rows dropped (missing critical fields): {dropped}")
    print(f"Non-critical nulls filled with default values.")
    print(f"Rows remaining: {frame.shape[0]}")



# 4. Fix Data Types
def fix_data_types():
    global cleaned_df

    if not require_data():
        return

    print_header("4. Fix Data Types")

    frame = (cleaned_df if cleaned_df is not None else df).clone()

    if "order_id" in frame.columns:
        frame = frame.with_columns(
            pl.col("order_id").cast(pl.Int64, strict=False).alias("order_id")
        )
        print("order_id   converted to integer (Int64)")

    if "sale_date" in frame.columns:
        frame = frame.with_columns(
            pl.col("sale_date")
              .str.strptime(pl.Date, format="%m/%d/%Y", strict=False)
              .alias("sale_date")
        )
        bad_dates = frame["sale_date"].is_null().sum()
        print(f"sale_date  converted to Date ({bad_dates} unparseable values set to null)")

    if "quantity" in frame.columns:
        frame = frame.with_columns(
            pl.col("quantity").cast(pl.Int32, strict=False).alias("quantity")
        )
        print("quantity   converted to integer (Int32)")

    if "unit_price" in frame.columns:
        frame = frame.with_columns(
            pl.col("unit_price").cast(pl.Float64, strict=False).alias("unit_price")
        )
        print("unit_price converted to decimal (Float64)")

    str_cols = ["customer_name", "region", "product_category", "product_name"]
    for col in str_cols:
        if col in frame.columns:
            frame = frame.with_columns(
                pl.col(col).str.strip_chars().str.to_titlecase().alias(col)
            )
    print("Text columns stripped of extra spaces and title-cased")

    cleaned_df = frame

    print("\nUpdated column types:")
    for col, dtype in zip(frame.columns, frame.dtypes):
        print(f"  {col:<22} {str(dtype)}")



# 5. Calculate Total Sales
def calculate_total_sales():
    global cleaned_df

    if not require_data():
        return

    print_header("5. Calculate Total Sales")

    frame = cleaned_df if cleaned_df is not None else df

    if "quantity" not in frame.columns or "unit_price" not in frame.columns:
        print("ERROR: Need both 'quantity' and 'unit_price' columns.")
        return

    frame = frame.with_columns([
        pl.col("quantity").cast(pl.Float64, strict=False),
        pl.col("unit_price").cast(pl.Float64, strict=False),
    ])

    frame = frame.with_columns(
        (pl.col("quantity") * pl.col("unit_price")).alias("total_sales")
    )

    cleaned_df = frame

    valid = frame.filter(pl.col("total_sales").is_not_null())

    print("'total_sales' column created (quantity x unit_price)")
    print(f"\nGrand Total Revenue : ${valid['total_sales'].sum():>12,.2f}")
    print(f"Average Order Value : ${valid['total_sales'].mean():>12,.2f}")
    print(f"Largest Single Order: ${valid['total_sales'].max():>12,.2f}")



# 6. Filter Invalid Data
def filter_invalid_data():
    global cleaned_df

    if not require_data():
        return

    print_header("6. Filter Invalid Data")

    frame = (cleaned_df if cleaned_df is not None else df).clone()
    original = frame.shape[0]

    if "quantity" in frame.columns:
        frame = frame.with_columns(pl.col("quantity").cast(pl.Float64, strict=False))
        bad = frame.filter(
            pl.col("quantity").is_null() | (pl.col("quantity") <= 0)
        ).shape[0]
        frame = frame.filter(
            pl.col("quantity").is_not_null() & (pl.col("quantity") > 0)
        )
        if bad:
            print(f"Removed {bad} rows with invalid quantity (null, zero, or negative)")

    if "unit_price" in frame.columns:
        frame = frame.with_columns(pl.col("unit_price").cast(pl.Float64, strict=False))
        bad = frame.filter(
            pl.col("unit_price").is_null() | (pl.col("unit_price") <= 0)
        ).shape[0]
        frame = frame.filter(
            pl.col("unit_price").is_not_null() & (pl.col("unit_price") > 0)
        )
        if bad:
            print(f"Removed {bad} rows with invalid unit_price (null, zero, or negative)")

    if "sale_date" in frame.columns and frame["sale_date"].dtype == pl.Date:
        bad = frame.filter(pl.col("sale_date").is_null()).shape[0]
        frame = frame.filter(pl.col("sale_date").is_not_null())
        if bad:
            print(f"Removed {bad} rows with unparseable sale_date")

    removed = original - frame.shape[0]
    cleaned_df = frame

    print(f"\nTotal rows removed : {removed}")
    print(f"Rows remaining     : {frame.shape[0]}")



# 7. Perform Analysis
def perform_analysis():
    if not require_data():
        return

    print_header("7. Perform Analysis")

    frame = cleaned_df if cleaned_df is not None else df

    if "total_sales" not in frame.columns:
        if "quantity" in frame.columns and "unit_price" in frame.columns:
            frame = frame.with_columns([
                pl.col("quantity").cast(pl.Float64, strict=False),
                pl.col("unit_price").cast(pl.Float64, strict=False),
            ]).with_columns(
                (pl.col("quantity") * pl.col("unit_price")).alias("total_sales")
            )
            print("Note: 'total_sales' was calculated on the fly for this analysis.")
        else:
            print("ERROR: Need 'quantity' and 'unit_price' columns to run analysis.")
            return

    total_rev = frame["total_sales"].drop_nulls().sum()
    print(f"Total Revenue: ${total_rev:,.2f}")

    if "region" in frame.columns:
        print("\nSales by Region:")
        by_region = (
            frame.group_by("region")
                 .agg(
                     pl.col("total_sales").sum().alias("revenue"),
                     pl.len().alias("orders")
                 )
                 .sort("revenue", descending=True)
        )
        for row in by_region.iter_rows(named=True):
            print(f"  {str(row['region']):<15}  ${row['revenue']:>10,.2f}  ({row['orders']} orders)")

    if "product_category" in frame.columns:
        print("\nTop Product Categories:")
        by_cat = (
            frame.group_by("product_category")
                 .agg(pl.col("total_sales").sum().alias("revenue"))
                 .sort("revenue", descending=True)
        )
        for i, row in enumerate(by_cat.iter_rows(named=True), 1):
            print(f"  {i}. {str(row['product_category']):<18}  ${row['revenue']:>10,.2f}")



# 8. Export Cleaned Data
def export_cleaned_data():
    if not require_data():
        return

    print_header("8. Export Cleaned Data")

    frame = cleaned_df if cleaned_df is not None else df

    path = input("Enter output filename (e.g. cleaned_sales.csv): ").strip()

    try:
        frame.write_csv(path)
        print(f"Saved to '{path}': {frame.shape[0]} rows, {frame.shape[1]} columns")
    except Exception as e:
        print(f"ERROR: Could not save file. {e}")



# 9. Detect Duplicate Orders (extra)
def detect_duplicates():

# Checks for order_id values that appear more than once
# Indicate duplicate transactions, system errors, or potential fraud

    if not require_data():
        return

    print_header("9. Detect Duplicate Orders")

    frame = cleaned_df if cleaned_df is not None else df

    if "order_id" not in frame.columns:
        print("ERROR: No 'order_id' column found.")
        return

    dupe_ids = (
        frame.group_by("order_id")
             .agg(pl.len().alias("count"))
             .filter(pl.col("count") > 1)
             .sort("count", descending=True)
    )

    if dupe_ids.is_empty():
        print("No duplicate order IDs found. Data looks clean.")
        return

    extra_rows = dupe_ids["count"].sum() - dupe_ids.shape[0]
    print(f"Found {dupe_ids.shape[0]} order ID(s) that appear more than once.")
    print(f"Extra duplicate rows: {extra_rows}")
    print()
    print(f"  {'order_id':<12}  {'occurrences'}")
    print(f"  {'-'*12}  {'-'*11}")
    for row in dupe_ids.iter_rows(named=True):
        print(f"  {str(row['order_id']):<12}  {row['count']}")

    show = input("\nShow the full duplicate rows? (y/n): ").strip().lower()
    if show == "y":
        dupe_order_ids = dupe_ids["order_id"]
        dupes = frame.filter(pl.col("order_id").is_in(dupe_order_ids))
        print(dupes.sort("order_id"))



# 10. Compliance Summary Report (extra)
def summary_report():

# Prints a summary of data quality and revenue metrics, useful for daily audit logs or compliance reporting.
    
    if not require_data():
        return

    print_header("10. Compliance Summary Report")

    raw   = df
    clean = cleaned_df if cleaned_df is not None else df

    print("\n--- Raw Data ---")
    print(f"Total records loaded  : {raw.shape[0]}")
    print(f"Total columns         : {raw.shape[1]}")

    null_totals = raw.select(pl.all().is_null().sum())
    total_nulls = sum(null_totals.row(0))
    null_pct    = (total_nulls / (raw.shape[0] * raw.shape[1])) * 100
    if null_pct > 10:
        risk = "HIGH"
    elif null_pct > 3:
        risk = "MEDIUM"
    else:
        risk = "LOW"
    print(f"Total null cells      : {total_nulls}")
    print(f"Null density          : {null_pct:.2f}%  (Risk: {risk})")

    print("\n--- Cleaned Data ---")
    rows_removed = raw.shape[0] - clean.shape[0]
    print(f"Records after cleaning: {clean.shape[0]}")
    print(f"Records removed       : {rows_removed} ({rows_removed / raw.shape[0] * 100:.1f}%)")

    if "total_sales" in clean.columns:
        sales = clean["total_sales"].cast(pl.Float64, strict=False).drop_nulls()
        print("\n--- Revenue Summary ---")
        print(f"Grand total revenue   : ${sales.sum():>12,.2f}")
        print(f"Average order value   : ${sales.mean():>12,.2f}")
        print(f"Minimum order value   : ${sales.min():>12,.2f}")
        print(f"Maximum order value   : ${sales.max():>12,.2f}")

    if "sale_date" in clean.columns and clean["sale_date"].dtype == pl.Date:
        print(f"\nDate range            : {clean['sale_date'].min()}  to  {clean['sale_date'].max()}")

    print("\nReport complete.")


# Main Menu
MENU = [
    ("1",  "Load data",                    load_data),
    ("2",  "Inspect data",                 inspect_data),
    ("3",  "Clean null values",            clean_null_values),
    ("4",  "Fix data types",               fix_data_types),
    ("5",  "Calculate total sales",        calculate_total_sales),
    ("6",  "Filter invalid data",          filter_invalid_data),
    ("7",  "Perform analysis",             perform_analysis),
    ("8",  "Export cleaned data",          export_cleaned_data),
    ("9",  "Detect duplicate orders",      detect_duplicates),
    ("10", "Compliance summary report",    summary_report),
    ("0",  "Exit",                         None),
]

def print_menu():
    status = f"Data loaded: {df.shape[0]} rows" if df is not None else "No data loaded"
    if cleaned_df is not None:
        status += "  |  Cleaning applied"
    print(f"\nStatus: {status}")
    print()
    for key, label, _ in MENU:
        note = "  (extra)" if key in ("9", "10") else ""
        print(f"  [{key:>2}]  {label}{note}")
    print()

def main():
    print("=" * 45)
    print("   Sales Transaction Data Cleaner")
    print("=" * 45)
    print()

    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        matched = False
        for key, label, fn in MENU:
            if choice == key:
                matched = True
                if fn is None:
                    print("\nGoodbye.")
                    sys.exit(0)
                fn()
                input("\nPress Enter to return to the menu...")
                break

        if not matched:
            print(f"'{choice}' is not a valid option. Please try again.")

if __name__ == "__main__":
    main()