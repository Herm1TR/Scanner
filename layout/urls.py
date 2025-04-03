from django.urls import path, include
from layout.views import floorplan_view, update_box_view
from rest_framework import routers
from .views import BoxViewSet, OperationLogViewSet


router = routers.DefaultRouter()
router.register(r'boxes', BoxViewSet)
router.register(r'logs', OperationLogViewSet)

urlpatterns = [
    path('', floorplan_view, name='floorplan'),
    path('update-box/', update_box_view, name='update_box'),
    path('api/', include(router.urls)),
]
