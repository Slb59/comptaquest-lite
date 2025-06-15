from django.test import TestCase
from django.utils import timezone
from datetime import date, timedelta
from secretbox.users.models import Member
from tests.factories.member import MemberFactory
from secretbox.dashboard.models import Todo
from django.core.exceptions import ValidationError


class TodoModelTests(TestCase):
    def setUp(self):
        """Setup method to create test data"""
        self.user = MemberFactory()
        self.todo = Todo.objects.create(
            user=self.user,
            state="todo",
            duration=timedelta(hours=1),
            description="Test task",
            appointment=timezone.now(),
            category="01-organisation",
            who="SLB",
            place="partout",
            periodic="01-none",
            date=date.today(),
            priority="1-highest",
            note="Test note"
        )

    def test_todo_creation(self):
        """Test that a Todo instance can be created"""
        self.assertEqual(self.todo.user, self.user)
        self.assertEqual(self.todo.state, "todo")
        self.assertEqual(self.todo.description, "Test task")
        self.assertEqual(self.todo.category, "01-organisation")
        self.assertEqual(self.todo.who, "SLB")
        self.assertEqual(self.todo.place, "partout")
        self.assertEqual(self.todo.periodic, "01-none")
        self.assertEqual(self.todo.priority, "01-none")

    def test_validate_element_success(self):
        """Test validate_element when new date is in the future"""
        new_date = date.today() + timedelta(days=1)
        result = self.todo.validate_element(new_date)
        self.assertTrue(result)
        self.assertEqual(self.todo.date, new_date)

    def test_validate_element_failure(self):
        """Test validate_element when new date is not in the future"""
        new_date = date.today() - timedelta(days=1)
        result = self.todo.validate_element(new_date)
        self.assertFalse(result)
        self.assertNotEqual(self.todo.date, new_date)

    def test_next_date_daily(self):
        """Test next_date with daily periodicity"""
        self.todo.periodic = "02-everyday"
        next_date = self.todo.next_date()
        expected_date = self.todo.date + timedelta(days=1)
        self.assertEqual(next_date, expected_date)

    def test_next_date_weekly(self):
        """Test next_date with weekly periodicity"""
        self.todo.periodic = "07-everyweek"
        next_date = self.todo.next_date()
        expected_date = self.todo.date + timedelta(days=7)
        self.assertEqual(next_date, expected_date)

    def test_report_element(self):
        """Test report_element method"""
        original_date = self.todo.date
        self.todo.report_element()
        self.assertEqual(self.todo.state, "report")
        self.assertEqual(self.todo.date, original_date + timedelta(days=1))

    def test_state_choices(self):
        """Test that state choices are valid"""
        valid_states = [state[0] for state in Todo.STATE_CHOICES]
        self.todo.state = "invalid_state"
        with self.assertRaises(ValueError):
            self.todo.save()
        self.todo.state = "todo"
        self.todo.save()  # Should not raise an error

    def test_priority_choices(self):
        """Test that priority choices are valid"""
        valid_priorities = [priority[0] for priority in Todo.PRIORITY_CHOICES]
        self.todo.priority = "invalid_priority"
        with self.assertRaises(ValueError):
            self.todo.save()
        self.todo.priority = "01-none"
        self.todo.save()  # Should not raise an error

    def test_category_choices(self):
        """Test that category choices are valid"""
        valid_categories = [category[0] for category in Todo.CATEGORY_CHOICES]

        # Test invalid category
        self.todo.category = "invalid_category"
        with self.assertRaises(ValidationError):
            self.todo.full_clean()
        
        # Test valid category
        self.todo.category = "01-organisation"
        try:
            self.todo.full_clean()  # This should not raise an error
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

    def test_who_choices(self):
        """Test that who choices are valid"""
        valid_who = [who[0] for who in Todo.WHO_CHOICES]
        self.todo.who = "invalid_who"
        with self.assertRaises(ValueError):
            self.todo.save()
        self.todo.who = "SLB"
        self.todo.save()  # Should not raise an error

    def test_place_choices(self):
        """Test that place choices are valid"""
        valid_places = [place[0] for place in Todo.PLACE_CHOICES]
        self.todo.place = "invalid_place"
        with self.assertRaises(ValueError):
            self.todo.save()
        self.todo.place = "partout"
        self.todo.save()  # Should not raise an error

    def test_periodic_choices(self):
        """Test that periodic choices are valid"""
        valid_periodic = [periodic[0] for periodic in Todo.PERIODIC_CHOICES]
        self.todo.periodic = "invalid_periodic"
        with self.assertRaises(ValueError):
            self.todo.save()
        self.todo.periodic = "01-none"
        self.todo.save()  # Should not raise an error