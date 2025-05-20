from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import forms as auth_forms
from .models import CQUser, MemberProfile


class LoginForm(auth_forms.AuthenticationForm):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.TextInput(attrs={
            'placeholder': _('Email'),
            'class': 'form-input',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Password'),
            'class': 'form-input'
        })
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive."),
                code='inactive',
            )


class CQUserCreationForm(auth_forms.UserCreationForm):
    """New Member Creation Form"""

    class Meta(auth_forms.UserCreationForm):
        model = CQUser
        fields = {"trigram", "email", "password"}


class CQUserChangeForm(auth_forms.UserChangeForm):
    """New Member Creation Form"""

    class Meta(auth_forms.UserCreationForm):
        model = CQUser
        fields = {"trigram", "email", "password"}


class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ["avatar"]
        widgets = {
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
        }
