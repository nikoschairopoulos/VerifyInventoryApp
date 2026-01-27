from inventory.models import ETS
import pandas as pd
from django.db.utils import IntegrityError
from datetime import datetime, timedelta


def run():
    year_now = datetime.now().year
    url = f"https://public.eex-group.com/eex/eua-auction-report/emission-spot-primary-market-auction-report-{year_now}-data.xlsx"
    try:
        url_df = pd.read_excel(url, header=5, usecols=['Date', "Auction Price €/tCO2"], parse_dates=['Date'])
        excel_year = year_now
    except Exception as e:
        print(f"Excel file for {year_now} not found, falling back to previous year.")
        fallback_year = year_now - 1
        fallback_url = f"https://public.eex-group.com/eex/eua-auction-report/emission-spot-primary-market-auction-report-{fallback_year}-data.xlsx"
        url_df = pd.read_excel(
            fallback_url,
            header=5,
            usecols=['Date', "Auction Price €/tCO2"],
            parse_dates=['Date']
        )
        excel_year = fallback_year
    print(f"Using ETS excel file for year {excel_year}.")

    url_df['Date'] = pd.to_datetime(url_df['Date'])
    # Reverse the order of days (so oldest appears first after expansion)
    first_row = url_df.iloc[0]
    last_date_online = first_row["Date"].date()
    last_price_online = float(first_row["Auction Price €/tCO2"])
    # print(last_date_online)

    # Get all registries from ETS table in reverse order (more recent on top)
    etss = ETS.objects.order_by('current_datetime').reverse()
    # Get the most recent ETS registry
    last_ets = etss[0]
    last_date_on_db = last_ets.current_datetime.date()
    last_price_on_db = last_ets.spot_price
    # print(last_date_on_db)

    # This is to ensure that there are not gaps more than 1 hour in db.
    hours_from_last_entry = int((datetime.now() - last_ets.current_datetime) / timedelta(hours=1))

    if hours_from_last_entry >= 2:
        print("A gap more than one hour is detected.")

        base = last_ets.current_datetime.replace(minute=0, second=0, microsecond=0)

        for i in range(1, hours_from_last_entry):
            datetime_new = base + timedelta(hours=i)
            ETS.objects.create(
                current_datetime=datetime_new,
                spot_price=last_price_on_db
            )
    else:
        print("No gaps detected in DB entries - hourly granularity.")

    # if last_date_online == last_date_on_db:
    if last_date_on_db == datetime.now().date():
        print("On the same day.")
        if last_price_online == last_price_on_db:
            # This usually is for all hours except 12:00 when price is updated
            print("No change for ETS price - expand for one more hour.")
            datetime_new = f'{datetime.now().date()} {datetime.now(tz=None).hour}:00:00'
            try:
                ETS.objects.create(
                    current_datetime=datetime_new,
                    spot_price=last_price_on_db
                )
            except IntegrityError:
                print("No data inserted - Data in DB are updated.")
        else:
            # This should happen at 12:00 where value is updated
            print("A change has been detected for ETS value - update the entire day with new value.")
            ETS.objects.filter(current_datetime__gte=last_date_on_db).update(spot_price=last_price_online)
            print("and add a new more entry for current timestamp.")
            datetime_new = f'{datetime.now().date()} {datetime.now(tz=None).hour}:00:00'
            ETS.objects.create(
                current_datetime=datetime_new,
                spot_price=last_price_online
            )
    elif datetime.now().date() > last_date_on_db:
        # This happens at 00:00 where date changes
        datetime_new = f'{datetime.now().date()} {datetime.now(tz=None).hour}:00:00'
        ETS.objects.create(
            current_datetime=datetime_new,
            spot_price=last_price_on_db
        )
        print("Continue to the next day with same ETS value - until updated.")
