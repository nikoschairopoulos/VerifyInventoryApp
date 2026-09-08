from django.shortcuts import get_object_or_404
from inventory.models import SimaPro_runs, Inventory, Component, Factor, FactorElectricityYear
from inventory.api.serializers import ComponentSerializer
from django.db.models import F, Value
from django.db.models.functions import Concat
from pprint import pprint


def run():
    # Use regex instead of contains because latter returned also PVC etc...
    # queryset = SimaPro_runs.objects.filter(name__iregex=r'(?i)(^|[^a-zA-Z])PV([^a-zA-Z]|$)').values()
    # queryset.update(name=Concat(Value('TEST '), F('name'), Value(' TEST')))

    # queryset = SimaPro_runs.objects.filter(name__startswith="TEST", name__endswith="TEST")
    # # queryset = SimaPro_runs.objects.filter(name__iregex=r'^TEST .* TEST$')
    # for qs in queryset:
    #     qs.name = qs.name[len("TEST "):-len(" TEST")]
    #     qs.save()

    # queryset = SimaPro_runs.objects.filter(name__iregex=r'(?i)(^|[^a-zA-Z])PV([^a-zA-Z]|$)')
    # for qs in queryset:
    #     print(qs.name)

    # rehouse_inv = Inventory.objects.filter(project_name="REHOUSE").first()
    #
    # query = Component.objects.filter(pk=1)[0]
    # ser = ComponentSerializer(query)

    # rehouse_inv.components.add(query)
    # rehouse_inv.components.remove(query)
    # factors = Factor.objects.all()
    #
    # print(len(factors.values('country').distinct()))
    # countries = [item["country"] for item in factors.values('country').distinct()]
    # print(countries)
    # for country in countries:
    #     Factor.objects.create(
    #         country=country,
    #         fuel="nuclear",
    #         co2_factor=0.0,
    #         primary_energy_factor=1.0
    #     )
    # ================================================
    # Update 11/2025 for PEF Factors for every country
    # ------------------------------------------------
    # Update with new PEF values as next:
    # Netherlands: 1.9
    # Portugal: 1.9
    # Finland: 2.1
    # France: 3
    # Everywhere else: 2.1
    # special_updates = {
    #     "Netherlands": 1.9,
    #     "Portugal": 1.9,
    #     "Finland": 2.1,
    #     "France": 3.0,
    # }
    # # Update every row with fuel="electricity" where PEF is not None and does not belong in special_updates
    # updated_rows = Factor.objects.filter(
    #     fuel="electricity",
    #     primary_energy_factor__isnull=False
    # ).exclude(
    #     country__in=special_updates.keys()
    # ).update(primary_energy_factor=2.1)

    # for country, new_pef in special_updates.items():
    #     rows_updated = Factor.objects.filter(
    #         country=country,
    #         fuel="electricity",
    #         primary_energy_factor__isnull=False
    #     ).update(primary_energy_factor=new_pef)

    switzerland_co2 = {
        1990: 0.03552312349778187,
        1991: 0.03552312349778187,
        1992: 0.03552312349778187,
        1993: 0.03552312349778187,
        1994: 0.03552312349778187,
        1995: 0.03552312349778187,
        1996: 0.03552312349778187,
        1997: 0.03552312349778187,
        1998: 0.03552312349778187,
        1999: 0.03552420482263086,
        2000: 0.03552569793002743,
        2001: 0.03552775968900657,
        2002: 0.0355306067796281,
        2003: 0.03553453854450517,
        2004: 0.03553996861346462,
        2005: 0.03554746870797572,
        2006: 0.03555782938960456,
        2007: 0.03557214444673922,
        2008: 0.03559192838524241,
        2009: 0.03561928052076582,
        2010: 0.03565711513538687,
        2011: 0.03570948617118631,
        2012: 0.03578204889147116,
        2013: 0.03588272321965391,
        2014: 0.03602266026767297,
        2015: 0.0362176767379826,
        2016: 0.03649043501651075,
        2017: 0.03687385905270159,
        2018: 0.03741669564518712,
        2019: 0.03819301033708347,
        2020: 0.03931938395395473,
        2021: 0.04098840970825018,
        2022: 0.04354023222377428,
        2023: 0.04763489354354958,
        2024: 0.05474309979724781
    }
    for year, value in switzerland_co2.items():
        FactorElectricityYear.objects.update_or_create(
            country="Switzerland",
            year=year,
            defaults={
                "measurement_co2": value
            }
        )

