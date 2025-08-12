from datetime import date

from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import activate, gettext_lazy as _

from secretbox.dashboard.todo_model import Todo
from secretbox.dashboard.todo_views import DashboardView
from tests.factories.member import MemberFactory
from tests.factories.todo import TodoFactory


class GetQuerysetByRightsTest(TestCase):
    def setUp(self):
        self.user1 = MemberFactory(email="test1@test.com", password="password")
        self.user2 = MemberFactory(email="test2@test.com", password="password")
        self.user3 = MemberFactory(email="test3@test.com", password="password")
        self.superuser = MemberFactory(email="super@test.com", password="password")
        self.superuser.is_superuser = True

        # 1: user is the owner of the todo
        self.todo_owner = TodoFactory(user=self.user1, description="created by user1")
        # 2: user is only a member of who
        self.todo_who = TodoFactory(
            user=self.user2, who=[self.user1], description="created by user2 for user1"
        )
        # 3: user is a member of both user and who
        self.todo_both = TodoFactory(
            user=self.user1, who=[self.user1], description="created by user1 for user1"
        )
        # 4: who has several members
        self.todo_many = TodoFactory(
            user=self.user2,
            who=[self.user1, self.user3],
            description="created by user2 for user1 and user3",
        )

        self.view = DashboardView()

    def test_superuser_can_see_all_todos(self):
        todos = self.view.get_queryset_by_rights(self.superuser)
        assert todos.count() == 4

        descriptions = set(t.description for t in todos)
        assert descriptions == {
            "created by user1",
            "created by user2 for user1",
            "created by user1 for user1",
            "created by user2 for user1 and user3",
        }

    def test_user1_sees_correct_todos(self):
        todos = self.view.get_queryset_by_rights(self.user1)
        assert todos.count() == 4
        descriptions = set(t.description for t in todos)
        assert descriptions == {
            "created by user1",
            "created by user2 for user1",
            "created by user1 for user1",
            "created by user2 for user1 and user3",
        }

    def test_no_duplicates_when_user_is_author_and_in_who(self):
        todos = self.view.get_queryset_by_rights(self.user1)
        # check that 4 objects are unique
        assert todos.count() == len(set(t.id for t in todos))

    def test_user2_only_sees_his_own(self):
        todos = self.view.get_queryset_by_rights(self.user2)
        assert todos.count() == 2
        descriptions = set(t.description for t in todos)
        assert descriptions == {
            "created by user2 for user1",
            "created by user2 for user1 and user3",
        }


class TodoTestMixin:
    def assertRedirectsToLogin(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def assertRedirectsToDashboard(self, response):
        if hasattr(response, "url"):
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, "/")
        else:
            # Debug
            print("Form errors:", response.context.get("form").errors)
            raise AssertionError(
                _("Pas de redirection : le formulaire a probablement échoué")
            )


class TodoCreateViewTest(TestCase, TodoTestMixin):
    def setUp(self):
        activate("fr")
        self.client = Client()
        self.user = MemberFactory(
            email="test@test.com", password="password", trigram="us1"
        )  # nosec: B106
        self.user.is_superuser = True
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

        # build a todo without saving it
        todo = TodoFactory.build(user=self.user)

        data = {
            "description": todo.description,
            "state": todo.state,
            "appointment": todo.appointment,
            "category": todo.category,
            "who": [self.user.pk],
            "place": todo.place,
            "periodic": todo.periodic,
            "planned_date": todo.planned_date.strftime("%Y-%m-%d"),
            "priority": todo.priority,
            "duration": todo.duration,
            "note": todo.note,
        }

        response = self.client.post(self.url, data)

        self.assertRedirectsToDashboard(response)
        assert Todo.objects.filter(
            description=todo.description, user=self.user
        ).exists()

    def test_create_todo_missing_required_field(self):
        self.client.force_login(self.user)

        # build a todo without saving it
        todo = TodoFactory.build(user=self.user)

        data = {
            # "description" is required but absent here
            "state": todo.state,
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
        self.user.is_superuser = True
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
        assert "Modifier l'entrée" in response.content.decode()

    def test_update_todo_valid_post(self):
        self.client.force_login(self.user)
        data = {
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
        }
        response = self.client.post(
            self.url,
            data,
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
        self.user.is_superuser = True
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
