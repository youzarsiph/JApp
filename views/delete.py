from JApp.models import *
from django.urls import reverse_lazy
from django.contrib.auth.views import get_user_model
from JApp.views.generic import MessageRequiredDeletionView, RequestUser, LoginRequiredMixin

User = get_user_model()


class UserDeletionView(LoginRequiredMixin, RequestUser, MessageRequiredDeletionView):
    model = User
    success_url = reverse_lazy('JApp:index')
    success_message = 'Account deleted successfully.'
    error_message = 'Error occurred while processing.'
