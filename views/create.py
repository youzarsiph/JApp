from JApp.models import *
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from JApp.forms.create import StyledUserCreationForm
from JApp.views.generic import CreationView, MessageRequiredCreationView

User = get_user_model()


class UserCreationView(CreationView):
    model = User
    form_class = StyledUserCreationForm
    success_url = reverse_lazy('JApp:login')

    def get_success_url(self):
        return reverse_lazy('JApp:edit_user', args=[self.object.pk])
