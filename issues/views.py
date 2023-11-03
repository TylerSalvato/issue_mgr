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
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from django.core.exceptions import PermissionDenied


class IssueListView(ListView):
    template_name = "issues/list.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo_status = Status.objects.get(name="todo")
        context["todo_list"] = Issue.objects.filter(
        status=todo_status).order_by("created_on").reverse()

        inprogress_status = Status.objects.get(name="inprogress")
        context["inprogress_list"] = Issue.objects.filter(
        status=inprogress_status).order_by("created_on").reverse()

        done_status = Status.objects.get(name="done")
        context["done_list"] = Issue.objects.filter(
        status=done_status
        ).order_by("created_on").reverse()
        return context
    
class IssueDetailView(DetailView):
    template_name = "issues/detail.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (
            context["issue"].status.name == "todo" and
            context["issue"].reporter != self.request.user
            ):
            raise PermissionDenied()
        if (
            context["issue"].status.name == "inprogress" and
            self.request.user.is_authenticated != True
            ):
            raise PermissionDenied()
        return context
    
class IssueCreateView(LoginRequiredMixin, CreateView):
    template_name = "issues/new.html"
    model = Issue
    fields = ["summary", "description", "assignee", "status"]

    # In your view
    def post(self, request, *args, **kwargs):
        form = YourForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.reporter = request.user  # Assign the reporter before saving
            issue.save()
            return redirect('success-url')  # Replace 'success-url' with your desired URL
        return render(request, 'your_template.html', {'form': form})


    if request.user.is_authenticated != True:
        new_issue = Issue.objects.create(
        title="Your Issue Title",
        description="Your Issue Description",
        reporter_id=request.user.id  # Set the reporter_id to the current user's ID
    )

    def form_valid(self, form):
        form.instance.role = self.request.user
        return super().form_valid(form)

    
class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "issues/edit.html"
    model = Issue
    fields = ["summary", "description", "assignee", "status"]

    def test_func(self):
        issue = self.get_object()
        return issue.role == self.request.user

class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "issues/delete.html"
    model = Issue
    success_url = reverse_lazy("list")

    def test_func(self):
        issue = self.get_object()
        return issue.role == self.request.user
    
class DraftIssueListView(ListView):
    template_name = "issues/list.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inprogress_status = Status.objects.get(name="inprogress")
        context["issue_list"] = Issue.objects.filter(
            status=inprogress_status
        ).filter(
            reporter=self.request.user
        ).order_by("created_on").reverse()
        return context
    
class ArchivedIssueListView(LoginRequiredMixin, ListView):
    template_name = "issues/list.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        done_status = Status.objects.get(name="done")
        context["done_list"] = Issue.objects.filter(
            status=done_status
        ).order_by("created_on").reverse()
        return context