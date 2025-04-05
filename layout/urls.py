from django.urls import path, include
from layout.views import floorplan_view, update_box_view, register
from rest_framework import routers
from .views import BoxViewSet, OperationLogViewSet
from django.contrib.auth import views as auth_views


router = routers.DefaultRouter()
router.register(r'boxes', BoxViewSet)
router.register(r'logs', OperationLogViewSet)

urlpatterns = [
    path('', floorplan_view, name='floorplan'),
    path('update-box/', update_box_view, name='update_box'),
    path('api/', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
]
