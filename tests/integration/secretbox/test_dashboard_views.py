from django.test import TestCase, Client
from tests.factories.member import MemberFactory
from tests.factories.todo import TodoFactory
from secretbox.dashboard.models import Todo
from django.urls import reverse
from datetime import date

class TodoDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = MemberFactory(email="test@test.com", password="password")
        print(self.user)
        self.todo1 = TodoFactory(user=self.user, state="todo")
        print(self.todo1)
        self.todo = TodoFactory(
            user=self.user,
            state="todo",            
            note="Note initiale",
        )
        self.url = reverse("dashboard:delete_todo", kwargs={"pk": self.todo.pk})
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.post(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertIn("login", response.url)

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
