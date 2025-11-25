from django.contrib import admin
from django.urls import path
from pets.views import home, AppointmentCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('appointments/new/', AppointmentCreateView.as_view(), name='appointment_create'),
]
