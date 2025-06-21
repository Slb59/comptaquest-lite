from django.contrib.auth import views as auth_views
from django.test import Client, TestCase
from django.urls import resolve, reverse

from secretbox.users import views
from tests.factories.member import MemberFactory


class TestUserUrls(TestCase):

    def test_login_url_resolves(self):
        url = reverse("users:login")
        self.assertEqual(resolve(url).func.view_class, views.CustomLoginView)

    def test_logout_url_resolves(self):
        url = reverse("users:logout")
        self.assertEqual(resolve(url).func.view_class, views.CustomLogoutView)

    def test_password_change_url_resolves(self):
        url = reverse("users:password_change")
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordChangeView)

    def test_password_change_done_url_resolves(self):
        url = reverse("users:password_change_done")
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordChangeDoneView)

    def test_password_reset_url_resolves(self):
        url = reverse("users:password_reset")
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetView)

    def test_password_reset_done_url_resolves(self):
        url = reverse("users:password_reset_done")
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetDoneView)

    def test_password_reset_confirm_url_resolves(self):
        url = reverse("users:password_reset_confirm", args=["uidb64", "token"])
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetConfirmView)

    def test_password_reset_complete_url_resolves(self):
        url = reverse("users:password_reset_complete")
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)

    def test_profile_url_resolves(self):
        url = reverse("users:profile")
        self.assertEqual(resolve(url).func.view_class, views.ProfileUpdateView)


class TestUserViews(TestCase):
    def setUp(self):
        self.member = MemberFactory(email="test@test.com", password="password")
        self.client = Client()

    def test_login_GET(self):
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_profile_GET_authenticated(self):
        self.client.login(email=self.member.email, password="password")
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 200)

    def test_profile_GET_unauthenticated(self):
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertRedirects(response, f'/login/?next={reverse("account:profile")}', status_code=302)

    def test_password_change_authenticated(self):
        self.client.login(email=self.member.email, password="password")
        response = self.client.get(reverse("users:password_change"))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_workflow(self):
        # Test password reset request
        response = self.client.get(reverse("users:password_reset"))
        self.assertEqual(response.status_code, 200)

        # Test password reset POST
        response = self.client.post(reverse("users:password_reset"), {"email": "test@example.com"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:password_reset_done"))

    def test_logout_authenticated(self):
        self.client.login(email=self.member.email, password="password")
        response = self.client.post(reverse("users:logout"))
        self.assertEqual(response.status_code, 200)
