from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from track.models import Profile, Child
from random import choice
from string import digits


class IndexView(ListView):
    template = "index.html"
    model = Child


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/"


class ChildCreateView(CreateView):
    model = Child
    success_url = "/"
    fields = ("first_name", "last_name", "parent")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.pin = ""
        for i in range(4):
            instance.pin += choice(digits)
        return super().form_valid(form)
