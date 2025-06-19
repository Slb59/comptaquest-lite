from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import NomadePosition

class EscapeVaultMapView(LoginRequiredMixin, TemplateView):
    template_name = "escapevault/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Create a base map centered around a specific location
        the_map = folium.Map(location=[48.8566, 2.3522], zoom_start=6) # Centered on France

        # Fetch all nomadic positions from the database
        positions = NomadePosition.objects.all()

        # Add markers for each position
        for position in positions:
            if position.latitude and position.longitude:
                folium.Marker(
                    location=[position.latitude, position.longitude],
                    popup=f"{position.name} ({position.city})",
                    tooltip=position.name
                ).add_to(the_map)

        # Convert the map to HTML
        the_map = the_map._repr_html_()        

        context["title"] = _("EscapeVault Map")
        context["logo_url"] = "/static/images/logo_ev.png"
        context['map'] = the_map
        return context
