from datetime import date

from django.contrib.auth.models import Group
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import activate

from secretbox.dashboard.todo_model import Todo
from tests.factories.member import MemberFactory
from tests.factories.todo import TodoFactory


class TodoTestMixin:
    def assertRedirectsToLogin(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def assertRedirectsToDashboard(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertEqual("/", response.url)


class TodoCreateViewTest(TestCase, TodoTestMixin):
    def setUp(self):
        activate("fr")
        self.client = Client()
        self.user = MemberFactory(
            email="test@test.com", password="password", trigram="us1"
        )  # nosec: B106
        group = Group.objects.create(name="comptaquest_access")
        self.user_with_group.groups.add(group)
        self.url = reverse("dashboard:add_todo")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirectsToLogin(response)

    def test_display_create_form(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert "Nouvelle entrée" in response.content.decode()

    def test_create_todo_valid_post(self):
        self.client.force_login(self.user)
        data = {
            "description": "Faire le ménage",
            "state": "todo",
            "appointment": "rdv",
            "category": "01-organisation",
            "who": "SLB",
            "place": "cantin",
            "periodic": "02-everyday",
            "planned_date": "2025-06-10",
            "priority": "4-normal",
            "duration": 30,
            "note": "À faire rapidement",
        }
        response = self.client.post(self.url, data)
        self.assertRedirectsToDashboard(response)
        assert Todo.objects.filter(
            description="Faire le ménage", user=self.user
        ).exists()

    def test_create_todo_missing_required_field(self):
        self.client.force_login(self.user)
        data = {
            # "description" est requis mais absent ici
            "state": "todo",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == 200  # Form is shown again

        form = response.context["form"]
        assert "description" in form.errors
        assert "Champ requis." in form.errors["description"]

        assert Todo.objects.count() == 0


class TodoUpdateViewTest(TestCase, TodoTestMixin):
    def setUp(self):
        activate("fr")
        self.client = Client()
        self.user = MemberFactory(email="test@test.com", password="password")
        self.todo1 = TodoFactory(user=self.user, state="todo")
        self.todo = TodoFactory(
            user=self.user,
            state="todo",
            note="Note initiale",
        )
        self.url = reverse("dashboard:edit_todo", kwargs={"pk": self.todo.pk})

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirectsToLogin(response)

    def test_logged_in_user_can_access_update_form(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        assert response.status_code == 200
        assert "Nouvelle entrée" in response.content.decode()

    def test_update_todo_valid_post(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.url,
            {
                "description": "Updated description",
                "state": self.todo.state,
                "category": self.todo.category,
                "who": self.todo.who,
                "place": self.todo.place,
                "priority": self.todo.priority,
                "periodic": self.todo.periodic,
                "planned_date": self.todo.planned_date,
                "appointment": self.todo.appointment,
                "duration": self.todo.duration,
                "note": self.todo.note or "",
            },
            follow=True,
        )
        assert response.status_code == 200
        self.todo.refresh_from_db()
        assert self.todo.description == "Updated description"

        def test_user_cannot_edit_other_users_todo(self):
            other_user = MemberFactory()
            self.client.force_login(other_user)
            response = self.client.get(self.url)
            assert response.status_code == 404


class TodoDeleteViewTest(TestCase, TodoTestMixin):
    def setUp(self):
        activate("fr")
        self.client = Client()
        self.user = MemberFactory(email="test@test.com", password="password")
        self.todo1 = TodoFactory(user=self.user, state="todo")
        self.todo = TodoFactory(
            user=self.user,
            state="todo",
            note="Note initiale",
        )
        self.url = reverse("dashboard:delete_todo", kwargs={"pk": self.todo.pk})

    def test_redirect_if_not_logged_in(self):
        response = self.client.post(self.url)
        self.assertRedirectsToLogin(response)

    def test_post_marks_todo_as_cancelled(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.state, "cancel")
        self.assertTrue(self.todo.note.startswith(f"*** supprimé {date.today()} ***"))
        self.assertRedirects(response, reverse("home"))

    def test_already_cancelled_todo_is_unchanged(self):
        self.todo.state = "cancel"
        self.todo.note = "*** supprimé Note initiale"
        self.todo.save()
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.state, "cancel")
        self.assertEqual(self.todo.note.count("*** supprimé"), 1)
        self.assertRedirects(response, reverse("home"))
