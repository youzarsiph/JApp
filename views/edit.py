from JApp.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from JApp.forms.main import UserEditForm
from django.contrib.auth.views import get_user_model
from JApp.views.generic import MessageRequiredEditView, RequestUser, LoginRequiredMixin

User = get_user_model()


class UserEditView(LoginRequiredMixin, RequestUser, MessageRequiredEditView):
    model = User
    form_class = UserEditForm
    success_url = reverse_lazy('JApp:profile')
    success_message = 'Account updated successfully.'
    error_message = 'Error occurred while processing.'

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if not (user.first_name and user.last_name and user.email):
            messages.success(request, 'Account created successfully, please fill in your information.')
        return super().get(request, *args, **kwargs)
