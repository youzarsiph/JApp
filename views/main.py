from django.views.generic import TemplateView
from JApp.views.mixins import DashboardMixin, LoginRequiredMixin
from JApp.views.create import *
from JApp.views.detail import *
from JApp.views.edit import *
from JApp.views.delete import *
from JApp.views.list import *


# Create your views here.
class IndexView(TemplateView):
    template_name = 'JApp/base/index.html'


class AboutView(TemplateView):
    template_name = 'JApp/base/about.html'


class ContactView(TemplateView):
    template_name = 'JApp/base/contact.html'


class DashboardView(DashboardMixin, TemplateView):
    template_name = 'JApp/base/dashboard.html'
    permission_required = 'JApp.view_example'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'JApp/authentication/profile.html'
