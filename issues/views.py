from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Issue, Status
from accounts.models import Role
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin)
from django.core.exceptions import PermissionDenied
from accounts.forms import CustomUser
from django.shortcuts import render, redirect

class IssueListView(ListView):
    template_name = "issues/list.html"
    model = Issue

class IssueDetailView(DetailView):
    template_name = "issues/detail.html"
    model = Issue

class IssueCreateView(UserPassesTestMixin, CreateView):
    template_name = "issues/new.html"
    model = Issue
    fields = ["summary", "description", "assignee", "status"]

    def form_valid(self, form):
        form.instance.reporter = self.request.user  # Set the reporter field
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user.is_product_owner

class IssueUpdateView(UserPassesTestMixin, UpdateView):
    template_name = "issues/edit.html"
    model = Issue
    fields = ["summary", "description", "assignee", "status"]
    success_url = reverse_lazy("detail")

    def test_func(self):
        post = self.get_object()
        return self.request.user.is_product_owner

class IssueDeleteView(UserPassesTestMixin, DeleteView):
    template_name = "issues/delete.html"
    model = Issue
    success_url = reverse_lazy("list")

    def test_func(self):
        post = self.get_object()
        return self.request.user.is_scrum_master
