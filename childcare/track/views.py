from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from track.models import Profile, Child
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from random import choice
from string import digits


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/"


class IndexView(TemplateView):
    template_name = "index.html"
    model = Child

    # def get_context_data(self):
    #     context = super().get_context_data()
    #     print(self.request.GET.get("pin"))
    #     if self.request.GET:
    #         pin = Child.objects.get(pin=self.request.GET.get("pin"))
    #         # context['pin'] = Child.objects.get(pin=self.request.GET.get("pin"))
    #         # child = Child.objects.get(id=1)
    #         print(pin.id)
    #         return HttpResponseRedirect(reverse("child_detail_view", args=(pin.id,)))
    #     return context


class Start_View(TemplateView):
    template_name = "start.html"
    model = Child
    
    def get(self, request):
        pin = request.GET["pin"]
        child = Child.objects.get(pin=pin)
        return HttpResponseRedirect(reverse("child_detail_view", args=(child.id,)))


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


class ChildDetailView(DetailView):
    model = Child
    success_url = "/"
