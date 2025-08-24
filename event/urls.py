from django.contrib import admin
from django.urls import path, include
from events.views import home, details, dashboard, create_event, delete_event, update_event, add_participant, add_category

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name='home'),
    path("details/<int:id>", details, name='details'),
    path("dashboard", dashboard, name='dashboard'),
    path("create-event", create_event, name='create-event'),
    path('delete-event/<int:id>/', delete_event, name='delete-event'),
    path('edit-event/<int:id>/', update_event, name='edit-event'),
    path('add-participant/<int:event_id>/', add_participant, name='add-participant'),
    path('add-category', add_category, name='add-category'),
    path("users/", include("users.urls")),
]
