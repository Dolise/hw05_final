from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm


class SignUp(CreateView):
    """Return rendered SignUp page.

    Subclass of CreateView

    Instance to CreationForm."""
    form_class = CreationForm
    success_url = reverse_lazy('signup')
    template_name = 'signup.html'
