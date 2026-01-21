from inventory.models import ETS
import pandas as pd
from django.db.utils import IntegrityError
from datetime import datetime, timedelta


def run():
    # cutoff_date = datetime(2025, 11, 4, 17)  # naive datetime, since your field is naive
    # ETS.objects.filter(current_datetime__gt=cutoff_date).delete()

    # q = ETS.objects.all()
    # q.delete()

    url = "https://public.eex-group.com/eex/eua-auction-report/emission-spot-primary-market-auction-report-2026-data.xlsx"
    url_df = pd.read_excel(url, header=5, usecols=['Date', "Auction Price €/tCO2"], parse_dates=['Date'])
    url_df['Date'] = pd.to_datetime(url_df['Date'])
    # Reverse the order of days (so oldest appears first after expansion)
    date = url_df.head(5).at[0, 'Date']
    price = url_df.head(5).at[0, 'Auction Price €/tCO2']
    last_date_online = date.date()
    last_price_online = price
    print(last_date_online)

    # Get all registries from ETS table in reverse order (more recent on top)
    etss = ETS.objects.order_by('current_datetime').reverse()
    # Get the most recent ETS registry
    last_ets = etss[0]
    last_date_on_db = last_ets.current_datetime.date()
    last_price_on_db = last_ets.spot_price
    print(last_date_on_db)

    # todays_entries = ETS.objects.filter(current_datetime__gte=last_date_on_db)

    # This is to ensure that there are not gaps more than 1 hour in db.
    hours_from_last_entry = int((datetime.now() - last_ets.current_datetime.replace(tzinfo=None))/ timedelta(hours=1))
    # print(hours_from_last_entry)
    if hours_from_last_entry >= 2:
        print("A gap more than one hour is detected.")
        # etss = ETS.objects.order_by('current_datetime').reverse()
        # Get the most recent ETS registry
        # last_ets = etss[0]
        cnt = 1
        datetime_new = pd.to_datetime(f'{last_ets.current_datetime.replace(tzinfo=None).date()} '
                        f'{last_ets.current_datetime.replace(tzinfo=None).hour + cnt}:00:00')
        # print(datetime_new)
        ETS.objects.create(
            current_datetime=datetime_new,
            spot_price=last_price_on_db
        )
        cnt += 1
        while cnt < hours_from_last_entry:
            datetime_new = pd.to_datetime(f'{datetime_new + timedelta(hours=1)}')
            print(datetime_new)
            ETS.objects.create(
                current_datetime=datetime_new,
                spot_price=last_price_on_db
            )
            cnt += 1
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
