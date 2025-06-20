from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Submit
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import \
    PasswordResetForm as DjangoPasswordResetForm
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _

from .models import CQUser, MemberProfile


class LoginForm(auth_forms.AuthenticationForm):
    email = forms.EmailField(
        label=_("Identifiant"),
        widget=forms.EmailInput(
            attrs={"placeholder": _("Votre adresse email"), "class": "form-input", "autofocus": True}
        ),
    )
    password = forms.CharField(
        label=_("Mot de passe"),
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": _("Votre mot de passe"), "class": "form-input"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "border p-8"
        # self.helper.form_method = 'GET'
        # self.helper.form_action = 'comptas:dashboard'
        self.helper.layout = Layout(
            # Div(
            #     Div('email', css_class="md:w-[50%]"),
            #     Div('password', css_class="md:w-[50%]"),
            #     css_class="md:flex md:justify-between"
            # ),
            "email",
            "password",
            Submit(
                "submit",
                "Se connecter",
                css_class="mt-4 focus:outline-none text-white bg-brown hover:bg-darkbrown focus:ring-4 focus:ring-yellow-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:focus:ring-yellow-900",
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError(_("Email ou mot de passe incorrect"))

        return cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive."),
                code="inactive",
            )


class CQUserCreationForm(auth_forms.UserCreationForm):
    """New Member Creation Form"""

    class Meta(auth_forms.UserCreationForm):
        model = CQUser
        fields = {"trigram", "email", "password"}


class CQUserChangeForm(auth_forms.UserChangeForm):
    """New Member Creation Form"""

    class Meta(auth_forms.UserChangeForm):
        model = CQUser
        fields = {"trigram", "email", "password"}


class ProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={"class": "form-input"}))
    trigram = forms.CharField(label=_("Trigram"), max_length=5, widget=forms.TextInput(attrs={"class": "form-input"}))
    avatar = forms.ImageField(label=_("Avatar"), required=False)

    class Meta:
        model = CQUser
        fields = ("email", "trigram", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"

        # Récupérer l'instance du profil utilisateur
        profile = self.instance._profile if hasattr(self.instance, "_profile") else None
        avatar_url = profile.get_avatar_url() if profile else "/static/images/default_avatar.png"

        # Ajouter un élément HTML pour afficher l'avatar actuel
        avatar_display = HTML(
            f"""
        <div class="flex justify-center mb-4">
            <img src="{avatar_url}" alt="Avatar" class="w-24 h-24 rounded-full">
        </div>
        """
        )

        self.helper.layout = Layout(
            "email",
            "trigram",
            avatar_display,
            "avatar",
            Submit(
                "submit",
                "Valider",
                css_class="button-valider",
            ),
        )
        # # Récupérer l'instance du profil utilisateur
        # if self.instance and hasattr(self.instance, '_profile'):
        #     profile = self.instance._profile
        #     self.initial['avatar'] = profile.avatar

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CQUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile, created = MemberProfile.objects.get_or_create(user=user)
            if "avatar" in self.cleaned_data and self.cleaned_data["avatar"]:
                profile.avatar = self.cleaned_data["avatar"]
                profile.save()
        return user


class PasswordResetForm(DjangoPasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].label = _("Email")
        self.fields["email"].widget = forms.EmailInput(
            attrs={"placeholder": _("Votre adresse email"), "class": "form-input", "autofocus": True}
        )

        self.helper = FormHelper()
        self.helper.form_class = "border p-8"
        self.helper.layout = Layout(
            "email",
            Submit(
                "submit",
                "Réinitialiser le mot de passe",
                css_class="mt-4 focus:outline-none text-white bg-brown hover:bg-darkbrown focus:ring-4 focus:ring-yellow-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:focus:ring-yellow-900",
            ),
        )
