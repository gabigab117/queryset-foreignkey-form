from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import AppointmentForm


def home(request):
    return render(request, 'pets/home.html')


class AppointmentCreateView(CreateView):
    form_class = AppointmentForm
    template_name = 'pets/appointment_form.html'
    success_url = reverse_lazy('home')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
