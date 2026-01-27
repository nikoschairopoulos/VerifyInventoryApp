from datetime import datetime, timedelta
import pandas as pd
from django.db import transaction
from inventory.models import ETS


def _excel_url_for_year(year: int) -> str:
    return (
        f"https://public.eex-group.com/eex/eua-auction-report/emission-spot-primary-market-auction-report-{year}-data.xlsx"
    )


def _read_daily_prices(year: int) -> pd.DataFrame:
    url = _excel_url_for_year(year)
    df = pd.read_excel(
        url,
        header=5,
        usecols=["Date", "Auction Price €/tCO2"],
        parse_dates=["Date"],
    ).dropna(subset=["Date", "Auction Price €/tCO2"])

    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df = df.sort_values("Date").rename(columns={"Auction Price €/tCO2": "price"})
    return df[["Date", "price"]]


def _build_hourly_rows(daily: pd.DataFrame, year: int) -> list[tuple[datetime, float]]:
    """
    24 rows/day. For today, writes until current hour.
    """
    now = datetime.now()
    today = now.date()
    max_hour_today = now.hour

    rows = []
    for d, p in zip(daily["Date"], daily["price"]):
        if d > today:
            continue    # no writing for future timestamps
        if d == today and d.year == year:
            hours = range(max_hour_today + 1)   # Timestamps only until current hour
        else:
            hours = range(24) # Timestamps for full day - 24 hours

        for h in hours:
            rows.append((datetime(d.year, d.month, d.day, h, 0 , 0), float(p)))

    return rows


def _upsert_hourly(rows: list[tuple[datetime, float]]):
    dts = [dt for dt, _ in rows]

    existing = ETS.objects.filter(current_datetime__in=dts).values_list("current_datetime", "id")
    existing_map = {dt: _id for dt, _id in existing}

    to_create, to_update = [], []
    for dt, price in rows:
        if dt in existing_map:
            to_update.append(ETS(id=existing_map[dt], current_datetime=dt, spot_price=price))
        else:
            to_create.append(ETS(current_datetime=dt, spot_price=price))

    with transaction.atomic():
        if to_create:
            ETS.objects.bulk_create(to_create, ignore_conflicts=True, batch_size=5000)
        if to_update:
            ETS.objects.bulk_update(to_update, ["spot_price"], batch_size=5000)

    return len(to_create), len(to_update)


def _delete_year(year: int):
    start = datetime(year, 1, 1, 0, 0, 0)
    end = datetime(year + 1, 1, 1, 0, 0, 0)
    deleted, _ = ETS.objects.filter(current_datetime__gte=start, current_datetime__lt=end).delete()
    return deleted


def run(*args):
    """
    Usage:
        python manage.py runscript orm_scripts3 --script-args 2025 2026
        python manage.py runscript orm_scripts3 --script-args reset 2025 2026

    Default (no args): current year only.
    """
    args = list(args)

    reset = False   # By default, no reset
    # If reset is passed as input argument:
    if args and args[0] == "reset":
        reset = True    # Set reset flag to True
        args = args[1:] # and get as input arguments the rest of args

    if args:
        years = [int(year) for year in args]
    else:
        years = [datetime.now().year]

    for year in years:
        if reset:
            deleted = _delete_year(year)
            print(f"[{year}] deleted rows: {deleted}")

        df = _read_daily_prices(year)

        start_date = datetime(year, 1, 1).date()
        end_date = df['Date'].max()

        full_days = pd.date_range(start_date, end_date, freq="D").date
        daily = (
            pd.DataFrame({"Date": full_days})
            .merge(df, on="Date", how="left")
            .sort_values("Date")
        )
        daily["price"] = daily["price"].ffill().bfill()

        rows = _build_hourly_rows(daily, year)
        created, updated = _upsert_hourly(rows)

        print(
            f"[{year}] range: {start_date} -> {min(end_date, datetime.now().date())} | "
            f"days: {len(daily)} | rows: {len(rows)} | created: {created} | updated: {updated}"
        )
    return
