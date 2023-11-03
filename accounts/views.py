from django.views.generic import CreateView
from .forms import CustomerUserCreationForm
from django.urls import reverse_lazy


# Create your views here.


class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomerUserCreationForm
    success_url = reverse_lazy("login")
