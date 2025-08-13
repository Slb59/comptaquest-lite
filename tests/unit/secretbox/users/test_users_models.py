from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import dateformat, timezone

from tests.factories.member import MemberFactory

Member = get_user_model()


class TestModelMember(TestCase):

    def setUp(self):
        self.member_1 = MemberFactory(email="member1@comptaquest.com", trigram="MB1")
        self.member_1.save()

    def test_create_user(self):
        user = MemberFactory(email="member2@comptaquest.com", trigram="MB2")
        self.assertEqual(user.email, "member2@comptaquest.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.first_name)
            self.assertIsNone(user.last_name)
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            Member.objects.create_user(trigram="")
        with self.assertRaises(TypeError):
            Member.objects.create_user(email="", trigram="foo")
        with self.assertRaises(ValueError):
            Member.objects.create_user(email="", password="foo", trigram="foo")

    def test_create_super_user(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="foo"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )

    def test_user_object_name_is_trigram(self):
        expected_object_name = f"{self.member_1.trigram}"
        self.assertEqual(expected_object_name, str(self.member_1))

    def test_user_profile_name_is_trigram(self):
        expected = f"Profile of {self.member_1.trigram}"
        self.assertEqual(expected, str(self.member_1.profile))

    def test_member_default_type_is_member(self):
        expected_object_name = "member"
        self.assertEqual(expected_object_name, self.member_1.usertype)

    def test_user_created_date_is_today(self):
        expected_object_name = f"{dateformat.format(timezone.now(), 'Y-m-d')}"
        format_user_created_date = f"{
            dateformat.format(self.member_1.profile.created_at, 'Y-m-d')
        }"
        self.assertEqual(expected_object_name, format_user_created_date)
