from django.contrib import admin
from django.urls import path
from events.views import home, details, dashboard, create_event, delete_event

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name='home'),
    path("details/<int:id>", details, name='details'),
    path("dashboard", dashboard, name='dashboard'),
    path("create-event", create_event, name='create-event'),
    path('delete-event/<int:id>/', delete_event, name='delete-event'),
]
