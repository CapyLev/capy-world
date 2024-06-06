from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .mixins import UserServersMixin


class RealmTemplateView(TemplateView, LoginRequiredMixin, UserServersMixin):
    pass
