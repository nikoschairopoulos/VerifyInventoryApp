from inventory.api.views import (
          ComponentViewSet,
          InventoryViewSet,
          RegressionValuesViewSet,
          ListInventory,
          LIBRARY_VERIFY,
          FactorViewSet,
          Components_by_technology,
          Inventory_technologies,
          Specific_inventory_plus_default,
          calculate_district_component_analytics,
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
          get_components_logs,
          give_picture_of_component_from_timestamp,
          regression_values,
          SimaPro_runsViewSet,
          get_embobied_eol_values,
          FormRepresentationVerifyApp,
          get_all_components_without_simapro_runs,
          Fetch_Specific_User_Custom_Plus_Defaults,
          GetComponentsForCalculationModule,
          ReportInfoComponents,
          DeletedComponentsViewSet,
          fetch_all_distinct_year_for_hourly_electricity_factors_for_a_country
        )
#out of this app views
from users.views import CreateUser

#from django.urls import path
from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"component",ComponentViewSet )
router.register(r"inventory", InventoryViewSet)
router.register(r"factor",FactorViewSet)
router.register(r"simapro_runs",SimaPro_runsViewSet)
router.register(r"deleted_component",DeletedComponentsViewSet)

#router.register(r"regression_values",RegressionValuesViewSet)

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
    path('get_components_logs/<int:lci_id>',get_components_logs.as_view(),name='logs'),
    path('give_picture_of_component_from_timestamp/<int:lci_id>',give_picture_of_component_from_timestamp.as_view(),name='reconstructions'),
    path('get_embodied_eol_values/<int:lci_id>/<str:rating>',get_embobied_eol_values.as_view(),name='embodied_eol'),
    path('get_component_form_representation',FormRepresentationVerifyApp.as_view(),name='component_form_representation'),
    path('get_all_components_without_simapro_runs',get_all_components_without_simapro_runs.as_view(),name='components_without_simaproruns'),
    path('user_components/<str:user_email>',Fetch_Specific_User_Custom_Plus_Defaults.as_view(),name='fetch_users_components'),
    path('create_new_lci_user',CreateUser.as_view(),name = 'createUser'),
    path('get_components',GetComponentsForCalculationModule.as_view(),name='calculation_module_components'),
    path('get_report_from_components',ReportInfoComponents.as_view(),name='report'),
    path('get_distinct_years_for_electricity_factors/<str:country>',fetch_all_distinct_year_for_hourly_electricity_factors_for_a_country.as_view(),name='hourly_factors_years'),
    path('get_verify_d_components',calculate_district_component_analytics.as_view(),name="verify_d_analytics")
    #path('regression_values_component/<int:lci_id>',regression_values.as_view(),name='regression_values')
    #path('/simapro_values',SimaPro_runsViewSet.as_view(),name = 'sima_pro_runs')
]



