from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect


REGISTRATION_SUCCESS_MESSAGE = _("Task created Successfully")
UPDATE_SUCCESS_MESSAGE = _("Task updated Successfully")
DELETE_SUCCESS_MESSAGE = _("Task deleted Successfully")
NOT_AUTHOR_MESSAGE = _("Only author can delete this task")


class IndexView(LoginRequiredMixin,
                ListView):
    model = Task
    template_name = 'tasks/index.html'


class DetailTask(DetailView):
    model = Task
    template_name = "tasks/detail.html"


class TaskRegistrate(LoginRequiredMixin,
                     SuccessMessageMixin,
                     CreateView):

    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:index')
    success_message = REGISTRATION_SUCCESS_MESSAGE

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin,
                 SuccessMessageMixin,
                 UpdateView):

    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:index')
    success_message = UPDATE_SUCCESS_MESSAGE


class TaskDelete(LoginRequiredMixin,
                 UserPassesTestMixin,
                 SuccessMessageMixin,
                 DeleteView):

    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:index')
    success_message = DELETE_SUCCESS_MESSAGE

    def test_func(self):
        return self.request.user.id == self.get_object().author.id

    def handle_no_permission(self):
        messages.error(self.request, NOT_AUTHOR_MESSAGE)
        return redirect(reverse_lazy('tasks:index'))
