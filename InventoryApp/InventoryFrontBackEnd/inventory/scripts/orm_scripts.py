from django.shortcuts import get_object_or_404
from inventory.models import SimaPro_runs, Inventory, Component, Factor
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
    special_updates = {
        "Netherlands": 1.9,
        "Portugal": 1.9,
        "Finland": 2.1,
        "France": 3.0,
    }
    # Update every row with fuel="electricity" where PEF is not None and does not belong in special_updates
    updated_rows = Factor.objects.filter(
        fuel="electricity",
        primary_energy_factor__isnull=False
    ).exclude(
        country__in=special_updates.keys()
    ).update(primary_energy_factor=2.1)

    for country, new_pef in special_updates.items():
        rows_updated = Factor.objects.filter(
            country=country,
            fuel="electricity",
            primary_energy_factor__isnull=False
        ).update(primary_energy_factor=new_pef)

