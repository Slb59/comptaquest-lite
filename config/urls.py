"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from comptaquest.comptas.views import DashboardView
from django.contrib.auth.mixins import LoginRequiredMixin

urlpatterns = [
    # admin urls
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", include("django_components.urls")),

    # home url
    # path("", DashboardView.as_view(), name="dashboard"),
    path('dashboard/', LoginRequiredMixin(TemplateView.as_view(template_name='dashboard.html')), 
         name='dashboard'),

    # app urls
    path("account/", include("comptaquest.users.urls")),
    path("comptas/", include("comptaquest.comptas.urls")),
    path("utils/", include("comptaquest.utils.urls")),
    path("healths/", include("comptaquest.healths.urls")),
    path("consos/", include("comptaquest.consos.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if apps.is_installed("pattern_library"):
    urlpatterns += [
        path("patterns/", include("pattern_library.urls")),
    ]
