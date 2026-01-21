from datetime import datetime, timedelta
import pandas as pd
from django.db import transaction
from inventory.models import ETS


def run():
    """
    This is a script created to handle inconsistencies created upon a year's change.
    Specifically, it removes any values filled in 2026 taken from the old 2025 file and replace them with the
    correct values for 2026.
    """
    cutoff = datetime(2026, 1, 1, 0, 0, 0)
    deleted, _ = ETS.objects.filter(current_datetime__gte=cutoff).delete()
    print(f"Deleted {deleted} ETS rows from 2026-01-01 and onwards.")
    # --- CONFIG ---
    URL_2026 = (
        "https://public.eex-group.com/eex/eua-auction-report/emission-spot-primary-market-auction-report-2026-data.xlsx"
    )
    START_DATE = datetime(2026, 1, 1).date()  # first day of current year
    COL_DATE = "Date"
    COL_PRICE = "Auction Price €/tCO2"

    # 1. Read daily prices from Excel
    df = pd.read_excel(
        URL_2026,
        header=5,
        usecols=[COL_DATE, COL_PRICE],
        parse_dates=[COL_DATE],
    )

    df = df.dropna(subset=[COL_DATE, COL_PRICE]).copy()
    df[COL_DATE] = pd.to_datetime(df[COL_DATE]).dt.date
    df = df.sort_values(COL_DATE).rename(columns={COL_PRICE: "price"})

    # Get last available date from excel
    END_DATE = df[COL_DATE].max()

    # 2. Build full daily range and forward-fill missing days
    full_days = pd.date_range(START_DATE, END_DATE, freq='D').date
    daily = (
        pd.DataFrame({COL_DATE: full_days})
        .merge(df[[COL_DATE, "price"]], on=COL_DATE, how='left')
        .sort_values(COL_DATE)
    )
    daily['price'] = daily["price"].ffill().bfill()

    # 3. Expand to hourly rows (24 per day except today)
    now = datetime.now()
    today = now.date()
    current_hour = now.hour
    hourly = []
    for d, p in zip(daily[COL_DATE], daily["price"]):
        if d < today:
            # For days older than today fill the full day (24 hours)
            hours = range(24)
        elif d == today:
            # If day is today, fill until current hour
            hours = range(current_hour + 1)
        else:
            # For future timestamps do nothing
            continue

        for h in hours:
            hourly.append((datetime(d.year, d.month, d.day, h, 0, 0), float(p)))

    # 4. Update or Insert to DB (bulk)
    dts = [dt for dt, _ in hourly]
    existing = ETS.objects.filter(current_datetime__in=dts).values_list("current_datetime", "id")
    existing_map = {dt: _id for dt, _id in existing}

    to_create = []
    to_update = []

    for dt, price in hourly:
        if dt in existing_map:
            to_update.append(ETS(id=existing_map[dt], currnet_datetime=dt, sport_price=price))
        else:
            to_create.append(ETS(current_datetime=dt, spot_price=price))

    # Now Bulk update and create in DB according to the to_update and to_create, respectively.
    with transaction.atomic():
        if to_create:
            ETS.objects.bulk_create(to_create, ignore_conflicts=True, batch_size=5000)
        if to_update:
            ETS.objects.bulk_update(to_update, ["spot_price"], batch_size=5000)

    print(
        f"ETS 2026 upsert completed | "
        f"Days: {len(daily)} | "
        f"Rows: {len(hourly)} | "
        f"Created: {len(to_create)} | "
        f"Updated: {len(to_update)} | "
        f"Range: {START_DATE} -> {END_DATE}"
    )