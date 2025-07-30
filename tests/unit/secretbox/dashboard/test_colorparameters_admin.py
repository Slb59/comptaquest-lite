from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase
from django.utils.translation import gettext_lazy as _

from secretbox.dashboard.admin import ColorParameterAdmin
from secretbox.dashboard.colorparameter_model import ColorParameter
from tests.factories.colorparameters import ColorParameterFactory


class MockRequest:
    pass


class ColorParameterAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = ColorParameterAdmin(ColorParameter, self.site)
        self.obj = ColorParameterFactory(color="#123ABC")
        self.request = RequestFactory().get("/admin/")

    def test_list_display_fields(self):
        expected_fields = ("priority", "periodic", "category", "place", "color_display")
        self.assertEqual(self.admin.get_list_display(self.request), expected_fields)

    def test_list_filter_fields(self):
        expected_filters = ("priority", "periodic", "category", "place")
        self.assertEqual(self.admin.list_filter, expected_filters)

    def test_search_fields(self):
        expected_search_fields = ("color",)
        self.assertEqual(self.admin.search_fields, expected_search_fields)

    def test_color_display_renders_correct_html(self):
        rendered = self.admin.color_display(self.obj)
        expected_html = '<div style="width: 60px; height: 20px; background-color: #123ABC; border: 1px solid #ccc;"></div>'
        self.assertHTMLEqual(rendered, expected_html)

    def test_color_display_label(self):
        self.assertEqual(self.admin.color_display.short_description, _("Couleur"))
