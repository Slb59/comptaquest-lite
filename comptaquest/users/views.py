from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, UpdateView
from django.contrib.auth import authenticate

from .forms import LoginForm
from .models import CQUser


class LoginView(FormView):
    
    form_class = LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("comptas:dashboard")

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, _("Email ou mot de passe incorrect"))
            return self.form_invalid(form)    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Connexion")
        context["logo_url"] = "/static/images/logo.png"
        return context


class LogoutView(LoginRequiredMixin, LogoutView):

    template_name = "registration/login.html"
    success_url = reverse_lazy("users:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Nettoyage supplémentaire si nécessaire
            pass
        if not request.session.test_cookie_worked():
            messages.error(request, "Les cookies doivent être activés pour cette fonctionnalité.")
            return redirect("users:login")
        return super().dispatch(request, *args, **kwargs)

    def get_next_page(self):
        # Redirection basée sur le dernier type d'utilisateur
        last_user_type = self.request.session.get("last_user_type")

        if last_user_type == CQUser.UserTypes.ACCOUNTANT:
            return reverse_lazy("accountant_dashboard")
        elif last_user_type == CQUser.UserTypes.SUPERMEMBER:
            return reverse_lazy("supermember_dashboard")
        return reverse_lazy("member_dashboard")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        if self.request.user.usertype == CQUser.UserTypes.MEMBER:
            # For member users, get or create their profile
            profile, created = MemberProfile.objects.get_or_create(user=self.request.user)
            return profile
        return None

    def get_form_class(self):
        if self.request.user.usertype == CQUser.UserTypes.MEMBER:
            return MemberProfileForm
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Your profile has been updated successfully."))
        return response

    def form_invalid(self, form):
        messages.error(self.request, _("Please correct the errors below."))
        return super().form_invalid(form)
