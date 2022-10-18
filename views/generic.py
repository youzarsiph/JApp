from django.views import View
from JApp.views.mixins import *
from django.http import FileResponse
from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView


class CreationView(CreateView):
    """
    CreateView with template set automatically according to folder structure.
    """


class DetailsView(DetailView):
    """
    DetailView with template set automatically according to folder structure.
    """
    pk_url_kwarg = 'id'


class ListingView(ListView):
    """
    ListView with template set automatically according to folder structure.
    """


class EditView(UpdateView):
    """
    UpdateView with template set automatically according to folder structure.
    """
    pk_url_kwarg = 'id'


class DeletionView(DeleteView):
    """
    DeleteView with template set automatically according to folder structure.
    """
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse_lazy('JApp:' + self.model._meta.verbose_name.lower() + '_list')


# Generic Views with Messages
class MessageRequiredCreationView(MessageMixinCreateView, CreationView):
    """
    CreationView with messages.
    You need to define success_message and error_message in subclasses.
    """


class MessageRequiredEditView(MessageMixinUpdateView, EditView):
    """
    EditView with messages.
    You need to define success_message and error_message in subclasses.
    """


class MessageRequiredDeletionView(MessageMixinDeleteView, DeletionView):
    """
    DeletionView with messages.
    You need to define success_message and error_message in subclasses.
    """


class ModelImageView(View):
    """
    A view that serves user uploaded images.
    """
    model = None

    def get(self, request, pk):
        if self.model is not None:
            obj = self.model.objects.get(id=pk)
            return FileResponse(open(obj.image.url[1:], 'rb'), as_attachment=True)
        else:
            raise ImproperlyConfigured('You need to configure the model field.')
