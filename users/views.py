from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
import decimal
import random
from datetime import date
import django_filters
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import F, Sum, Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView, View, FormView, ListView
from django.http import Http404
from django.views.generic import DetailView, ListView, RedirectView, DeleteView, UpdateView, CreateView
from .models import *
from .forms import *
from django.shortcuts import render
# Create your views here.
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, RedirectView, DeleteView, \
    UpdateView, CreateView
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DeleteView, UpdateView, View, \
    FormView, ListView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.base import TemplateView
import requests
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Button, Row, Column
from django.forms import DateTimeField
from django.db.models import Avg, Case, Count, F
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import get_template
from django.template import Context
from django.views.generic.base import TemplateView
from .models import *
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, \
    UserPassesTestMixin, \
    PermissionRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django_filters.views import FilterView
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                     PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'model_update_form.html'
    permission_denied_message = _("You don't have permission to see this page")
    raise_exception = True
    success_message = _("User updated successfully")
    permission_required = 'users.change_user'

    def test_func(self):
        return self.request.user == self.get_object() or self.request.user.is_superuser

    # fields = ["groups"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.get_object().username})

    # def get_object(self):
    #     return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        # messages.add_message(
        #     self.request, messages.INFO, _("Infos successfully updated")
        # )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserPasswordUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                             SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserPasswordUpdateForm
    template_name = 'model_update_form.html'
    permission_denied_message = _("You don't have permission to see this page")
    raise_exception = True
    success_message = _("User updated successfully")

    # permission_required = 'users.change_user'

    def test_func(self):
        return self.request.user == self.get_object() or self.request.user.is_superuser

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.get_object().username})

    def form_valid(self, form):
        return super().form_valid(form)


user_password_update_view = UserPasswordUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin,
                     PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_denied_message = _("You don't have permission to see this page")
    raise_exception = True
    model = User
    success_message = _("User created successfully")
    permission_required = 'users.add_user'
    form_class = UserCreateForm
    template_name = 'model_form.html'

    def test_func(self):
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Ajouter un utilisateur")
        context['cancelurl'] = self.get_success_url()
        return context

    def get_success_url(self):
        return reverse('main:home-view')


# #############################################################################
# #                                User                                      # #
# #############################################################################


class UserFilterSet(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['groups']


class UserFiltreFormHelper(FormHelper):
    form_action = '#POST'
    form_method = 'POST'
    layout = Layout(
        Fieldset(
            None,
            Div( 
                Div(
                    'groups', css_class="col-sm-12"
                ),
                css_class='row'
            ),
        ),
    )
class UserListView(LoginRequiredMixin, UserPassesTestMixin,
                   PermissionRequiredMixin, FilterView):
    model = User
    filter_class = UserFilterSet
    formhelper_class = UserFiltreFormHelper
    context_filter_name = 'filter'
    paginate_by = 20
    ordering = ['username']
    permission_denied_message = _("You don't have permission to see this page")
    raise_exception = True
    permission_required = 'users.view_user'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_filter_name] = self.filter
        return context

    def test_func(self):
        return self.request.user.is_superuser
