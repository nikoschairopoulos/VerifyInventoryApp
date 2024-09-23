from inventory.api.views import (
          ComponentViewSet,
          InventoryViewSet,
          ListInventory,
          LIBRARY_VERIFY,
          FactorViewSet,
          Components_by_technology,
          Inventory_technologies,
          Specific_inventory_plus_default,
          find_fuel_factors_specific_country,
          inventory_without_components,
          only_main_inventory,
          CreateComponentFromExcell,
          IsAdminUser,
          ImportElectricityData,
          get_hourly_electricity_fuel_factors,
          ImportElectricityDataYearly,
          get_yearly_electricity_fuel_factors,
          get_countries_hourly_yearly_electricity_factors,
          get_components_logs
        )

#from django.urls import path
from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"component",ComponentViewSet )
router.register(r"inventory", InventoryViewSet)
router.register(r"factor",FactorViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("library/<int:pk>/",LIBRARY_VERIFY.as_view(),name="Library_Getter"),
    path("userInventories/",ListInventory.as_view(),name="List_Inventory_of_User"),
    path("component/<str:Technology_key>",Components_by_technology.as_view(),name="components_of_specific_technology"),
    path("technologies/",Inventory_technologies.as_view(),name="inventory_technologies"),
    path("verify/inventory/<int:pk>",Specific_inventory_plus_default.as_view(),name="verify_connections"),
    path("factors/<str:country>",find_fuel_factors_specific_country.as_view(),name='fuel_factors_specific_country'),
    path("verify/all_inventories",inventory_without_components.as_view(),name='all_inventories'),
    path("verify/component_main_inventory",only_main_inventory.as_view(),name='all_main_components'),
    path("excell_create",CreateComponentFromExcell.as_view(),name='create_components_from_excell'),
    path("is_admin_user",IsAdminUser.as_view(),name='is_admin_user'),
    path('load_electricity_measurements',ImportElectricityData.as_view(),name='import_electricity_data_hourly'),
    path('get_electricity_measurements/<str:country>/<int:year>', get_hourly_electricity_fuel_factors.as_view(),name='get_electricity_factors'),
    path('load_electricity_measurements_yearly',ImportElectricityDataYearly.as_view(),name='import_electricity_data_yearly'),
    path('get_electricity_measurements_yearly/<str:country>',get_yearly_electricity_fuel_factors.as_view(),name='get_yearly_electricity_factors'),
    path('get_countries_hourly_yearly', get_countries_hourly_yearly_electricity_factors.as_view(),name='countries_electricity_support'),
    path('get_components_logs/<int:lci_id>',get_components_logs.as_view(),name='logs')
]



