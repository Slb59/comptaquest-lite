from django.shortcuts import redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import LoginForm
from django.utils.translation import gettext_lazy as _
from .models import CQUser


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        # Redirection basée sur le type d'utilisateur
        if user.usertype == CQUser.UserTypes.ACCOUNTANT:
            return redirect(reverse_lazy('accountant_dashboard'))
        elif user.usertype == CQUser.UserTypes.SUPERMEMBER:
            return redirect(reverse_lazy('supermember_dashboard'))
        return redirect(reverse_lazy('member_dashboard'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Login')
        return context