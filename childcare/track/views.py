from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from track.models import Profile, Child, Time
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse, reverse_lazy
from random import choice
from string import digits
from datetime import datetime


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
    # model = Child

    def get(self, request):
        pin = request.GET["pin"]
        try:
            child = Child.objects.get(pin=pin)
            check = Time.objects.filter(child=child).first()
            if check:
                if not check.on_premise:
                    return HttpResponseRedirect(reverse("checkin_create_view", args=(child.id,)))
                return HttpResponseRedirect(reverse("checkin_update_view", args=(check.id,)))
        except ObjectDoesNotExist:
            return HttpResponseRedirect("/")


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


class CheckinCreateView(CreateView):
    model = Time
    success_url = "/"
    fields = ("on_premise", )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["child"] = Child.objects.all()
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.child = Child.objects.get(id=self.kwargs['pk'])
        if instance.on_premise:
            return super().form_valid(form)
        return super().form_invalid(form)


class CheckinUpdateView(UpdateView):
    model = Time
    success_url = "/"
    fields = ("on_premise", )

    def form_valid(self, form):
        instance = form.save(commit=False)
        if not instance.on_premise:
            instance.check_out = datetime.now()
            return super().form_valid(form)
        return super().form_invalid(form)


class StaffListView(ListView):
    model = Child
    success_url = reverse_lazy("index_view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["child"] = Child.objects.all()
        context["time"] = Time.objects.all()
        return context


class ProfileListView(ListView):
    model = Profile
    success_url = reverse_lazy("index_view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["child"] = Child.objects.all()
        context["time"] = Time.objects.all()
        return context
