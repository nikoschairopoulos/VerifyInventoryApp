from inventory.api.views import (
          ComponentViewSet,
          InventoryViewSet,
          ListInventory,
          LIBRARY_VERIFY)
#from django.urls import path
from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"component",ComponentViewSet )
router.register(r"inventory", InventoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("library/<int:pk>/",LIBRARY_VERIFY.as_view(),name="Library_Getter"),
    path("userInventories/",ListInventory.as_view(),name="List_Inventory_of_User")
]



