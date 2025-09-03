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
    factors = Factor.objects.all()

    print(len(factors.values('country').distinct()))
    countries = [item["country"] for item in factors.values('country').distinct()]
    print(countries)
    for country in countries:
        Factor.objects.create(
            country=country,
            fuel="nuclear",
            co2_factor=0.0,
            primary_energy_factor=1.0
        )


