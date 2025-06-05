from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.auth.views import \
    PasswordResetView as DjangoPasswordResetView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from .forms import LoginForm, PasswordResetForm, ProfileUpdateForm
from .models import CQUser


class LoginView(DjangoLoginView):

    form_class = LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
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
        context["logo_url"] = "/static/images/logo_sb.png"
        return context

    def get_success_url(self):

        next_page = success_url
        if next_page == "":
            next_page = "/"  # if next param is not available, then redirect the user to the homepage after login.

        return next_page

    def form_invalid(self, form):
        response = super().form_invalid(form)
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        if next_url:
            return redirect(f"{self.request.path}?next={next_url}")
        return response


class LogoutView(LoginRequiredMixin, DjangoLogoutView):

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
    model = CQUser
    form_class = ProfileUpdateForm
    template_name = "secretbox/profile.html"
    success_url = reverse_lazy("dashboard")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["title"] = _("Vos données")
        context["logo_url"] = "/static/images/logo_sb.png"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Your profile has been updated successfully."))
        return response

    def form_invalid(self, form):
        messages.error(self.request, _("Please correct the errors below."))
        return super().form_invalid(form)


class PasswordResetView(DjangoPasswordResetView):
    form_class = PasswordResetForm
    template_name = "registration/password_reset.html"
    success_url = reverse_lazy("users:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Reinitialisation du mot de passe")
        context["logo_url"] = "/static/images/logo-sb.png"
        return context


