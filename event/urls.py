from django.contrib import admin
from django.urls import path
from events.views import home, details, dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name='home'),
    path("details/<int:id>", details, name='details'),
    path("dashboard", dashboard, name='dashboard'),
]
