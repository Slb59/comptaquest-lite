from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from django.utils.translation import gettext_lazy as _
from django.db import models


@register_setting(icon='user')
class CustomAuthSettings(BaseSetting):
    login_page_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Login page title')
    )
    login_page_subtitle = models.TextField(
        blank=True,
        verbose_name=_('Login page subtitle')
    )

    panels = [
        FieldPanel('login_page_title'),
        FieldPanel('login_page_subtitle'),
    ]

    class Meta:
        abstract = True
