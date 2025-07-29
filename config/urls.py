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

from secretbox.dashboard.contact_views import ContactFormView
from secretbox.dashboard.todo_views import DashboardView
from secretbox.users.views import LoginView

urlpatterns = [
    # admin urls
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    # path("", include("django_components.urls")),
    # home url
    path("", DashboardView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("dashboard/", include("secretbox.dashboard.urls")),
    path("contact/", ContactFormView.as_view(), name="contact"),
    # comptaquest urls
    path("account/", include("secretbox.users.urls")),
    path("cq/comptas/", include("comptaquest.comptas.urls")),
    path("cq/utils/", include("comptaquest.utils.urls")),
    path("cq/healths/", include("comptaquest.healths.urls")),
    path("cq/consos/", include("comptaquest.consos.urls")),
    # potionrun urls
    path("pr/performances/", include("potionrun.performances.urls")),
    # diarylab urls
    path("diarylab/", include("diarylab.urls")),
    path("escapevault/", include("escapevault.urls")),
    path("sami/", include("sami.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if apps.is_installed("pattern_library"):
    urlpatterns += [
        path("patterns/", include("pattern_library.urls")),
    ]
