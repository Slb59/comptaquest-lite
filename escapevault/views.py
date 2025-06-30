import folium
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)

from .forms import EscapeVaultForm
from .models import NomadePosition


class EscapeVaultMapView(LoginRequiredMixin, TemplateView):
    template_name = "escapevault/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Create a base map centered around a specific location
        the_map = folium.Map(location=[48.8566, 2.3522], zoom_start=7)  # Centered on France

        # Fetch all nomadic positions from the database
        positions = NomadePosition.objects.all()

        # Add markers for each position
        for position in positions:

            icon = folium.CustomIcon(
                icon_image=position.get_category_image(),
                icon_size=(50, 50),
                icon_anchor=(0, 0),
            )

            if position.latitude and position.longitude:

                edit_url = reverse("escapevault:edit_position", kwargs={"pk": position.pk})
                edit_url += f"?next={self.request.get_full_path()}"
                popup_html = f"""
                <div>
                    <a href="{edit_url}" target="_blank" rel="noopener noreferrer">
                        Modifier
                    </a>
                </div>"""

                folium.Marker(
                    location=[position.latitude, position.longitude],
                    popup=folium.Popup(popup_html, max_width=250),
                    tooltip=f"{position.name} ({position.opening_date}-{position.closing_date})",
                    icon=icon,
                ).add_to(the_map)

        # Convert the map to HTML
        the_map = the_map._repr_html_()

        context["title"] = _("EscapeVault Map")
        context["logo_url"] = "/static/images/logo_ev.png"
        context["map"] = the_map
        return context


class EscapeVaultListView(LoginRequiredMixin, ListView):
    model = NomadePosition
    template_name = "escapevault/escapevault_list.html"
    context_object_name = "positions"

    def get_queryset(self):
        return NomadePosition.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("EscapeVault Liste")
        context["logo_url"] = "/static/images/logo_ev.png"
        return context


class EscapeVaultCreateView(LoginRequiredMixin, CreateView):
    model = NomadePosition
    form_class = EscapeVaultForm
    template_name = "escapevault/add_position.html"
    success_url = reverse_lazy("escapevault:list_positions")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("EscapeVault nouvelle Position")
        context["logo_url"] = "/static/images/logo_ev.png"
        return context


class EscapeVaultEditView(LoginRequiredMixin, UpdateView):
    model = NomadePosition
    form_class = EscapeVaultForm
    template_name = "escapevault/edit_position.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        next_url = self.request.GET.get("next")
        if next_url:
            form.fields["next"] = forms.CharField(widget=forms.HiddenInput(), initial=next_url, required=False)
        return form

    def get_success_url(self):
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        if next_url:
            return next_url
        return reverse("escapevault:list_positions")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _(f"{self.object.name}")
        context["logo_url"] = "/static/images/logo_ev.png"
        return context


class EscapeVaultDeleteView(LoginRequiredMixin, DeleteView):
    model = NomadePosition
    template_name = "escapevault/delete_position.html"
    success_url = reverse_lazy("escapevault:list_positions")
