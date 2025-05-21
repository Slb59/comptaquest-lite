from django.shortcuts import redirect
from django.views.generic import FormView, UpdateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import LoginForm
from django.utils.translation import gettext_lazy as _
from .models import CQUser
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('comptas:dashboard')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        # Redirection basée sur le type d'utilisateur
        # if user.usertype == CQUser.UserTypes.ACCOUNTANT:
        #     return redirect(reverse_lazy('accountant_dashboard'))
        # elif user.usertype == CQUser.UserTypes.SUPERMEMBER:
        #     return redirect(reverse_lazy('supermember_dashboard'))
        # return redirect(reverse_lazy('member_dashboard'))
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Login')
        return context

class LogoutView(LoginRequiredMixin, LogoutView):

    template_name = 'registration/login.html'
    success_url = reverse_lazy("users:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Nettoyage supplémentaire si nécessaire
            pass
        if not request.session.test_cookie_worked():
            messages.error(request, "Les cookies doivent être activés pour cette fonctionnalité.")
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)

    def get_next_page(self):
        # Redirection basée sur le dernier type d'utilisateur
        last_user_type = self.request.session.get('last_user_type')
        
        if last_user_type == CQUser.UserTypes.ACCOUNTANT:
            return reverse_lazy('accountant_dashboard')
        elif last_user_type == CQUser.UserTypes.SUPERMEMBER:
            return reverse_lazy('supermember_dashboard')
        return reverse_lazy('member_dashboard')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        if self.request.user.usertype == CQUser.UserTypes.MEMBER:
            # For member users, get or create their profile
            profile, created = MemberProfile.objects.get_or_create(
                user=self.request.user
            )
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