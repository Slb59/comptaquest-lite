from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from tests.factories.member import MemberFactory
from tests.factories.todo import TodoFactory


class TestTodoModel(TestCase):
    def setUp(self):
        """Setup method to create test data"""
        self.user = MemberFactory()
        self.todo = TodoFactory(user=self.user, state="todo")

    def test_todo_creation(self):
        """Test that a Todo instance can be created"""
        self.assertEqual(self.todo.user, self.user)
        self.assertEqual(self.todo.state, "todo")

    def test_validate_element_success(self):
        """Test validate_element when new date is in the future"""
        new_date = self.todo.planned_date + timedelta(days=1)
        result = self.todo.validate_element(new_date)
        self.assertTrue(result)
        self.assertEqual(self.todo.planned_date, new_date)

    def test_validate_element_failure(self):
        """Test validate_element when new date is not in the future"""
        new_date = self.todo.planned_date - timedelta(days=1)
        result = self.todo.validate_element(new_date)
        self.assertFalse(result)
        self.assertNotEqual(self.todo.planned_date, new_date)

    def test_next_date_daily(self):
        """Test next_date with daily periodicity"""
        self.todo.periodic = "02-everyday"
        next_date = self.todo.next_date()
        expected_date = self.todo.planned_date + timedelta(days=1)
        self.assertEqual(next_date, expected_date)

    def test_next_date_weekly(self):
        """Test next_date with weekly periodicity"""
        self.todo.periodic = "07-everyweek"
        next_date = self.todo.next_date()
        expected_date = self.todo.planned_date + timedelta(days=7)
        self.assertEqual(next_date, expected_date)

    def test_report_element(self):
        """Test report_element method"""
        mock_date = date(2025, 6, 24)

        self.todo.report_date = None

        # call report_element method
        self.todo.report_element(mock_date)

        # Test valid state
        self.assertEqual(self.todo.state, "report")
        self.assertEqual(self.todo.planned_date, mock_date + timedelta(days=1))
        self.assertEqual(self.todo.report_date, mock_date)

    def test_state_choices(self):
        """Test that state choices are valid"""

        # Test invalid state
        self.todo.state = "invalid_state"
        with self.assertRaises(ValidationError):
            self.todo.full_clean()

        # Test valid state
        self.todo.state = "todo"
        try:
            self.todo.full_clean()  # This should not raise an error
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

    def test_priority_choices(self):
        """Test that priority choices are valid"""

        # Test invalid priority
        self.todo.priority = "invalid_priority"
        with self.assertRaises(ValidationError):
            self.todo.full_clean()

        # Test valid priority
        self.todo.priority = "1-highest"
        try:
            self.todo.full_clean()  # This should not raise an error
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

    def test_category_choices(self):
        """Test that category choices are valid"""

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

        # Test invalid who
        self.todo.who = "invalid_who"
        with self.assertRaises(ValidationError):
            self.todo.full_clean()

        # Test valid who
        self.todo.who = "SLB"
        try:
            self.todo.full_clean()  # This should not raise an error
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

    def test_place_choices(self):
        """Test that place choices are valid"""

        # Test invalid place
        self.todo.place = "invalid_place"
        with self.assertRaises(ValidationError):
            self.todo.full_clean()

        # test valid place
        self.todo.place = "partout"
        try:
            self.todo.full_clean()
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

    def test_periodic_choices(self):
        """Test that periodic choices are valid"""

        # test invalid periodic
        self.todo.periodic = "invalid_periodic"
        with self.assertRaises(ValidationError):
            self.todo.full_clean()

        # test valid periodic
        self.todo.periodic = "01-none"
        try:
            self.todo.full_clean()
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

    def test_new_day_with_done_state(self):

        mock_date = date(2025, 6, 24)

        # Create an instance of YourModel with state "done"
        instance = TodoFactory(report_date=date(2025, 10, 9), planned_date=date(2025, 10, 9), state="done")

        # Call the new_day method
        instance.new_day(mock_date)

        # Refresh the instance from the database
        instance.refresh_from_db()

        # Check if the dates are not updated and state remains "done"
        report_date_expected = date(2025, 10, 9)
        self.assertEqual(instance.report_date, report_date_expected)
        planned_date_expected = date(2025, 10, 9)
        self.assertEqual(instance.planned_date, planned_date_expected)
        self.assertEqual(instance.state, "done")

    def test_new_day_with_non_done_state_and_planned_date_in_future(self):

        mock_date = date(2025, 6, 24)

        # Create an instance of YourModel with state other than "done"
        instance = TodoFactory(
            report_date=None,
            planned_date=date(2025, 6, 25),
            state="todo",
        )

        # Call the new_day method
        instance.new_day(mock_date)

        # Refresh the instance from the database
        instance.refresh_from_db()

        # Check if the dates are updated and state is set to "report"
        report_date_expected = None
        self.assertEqual(instance.report_date, report_date_expected)
        planned_date_expected = date(2025, 6, 25)
        self.assertEqual(instance.planned_date, planned_date_expected)
        self.assertEqual(instance.state, "todo")

    def test_new_day_with_non_done_state_and_planned_date_is_past(self):

        mock_date = date(2025, 6, 24)

        # Create an instance of YourModel with state other than "done"
        instance = TodoFactory(report_date=date(2025, 6, 20), planned_date=date(2025, 6, 20), state="todo")

        # Call the new_day method
        instance.new_day(mock_date)

        # Refresh the instance from the database
        instance.refresh_from_db()

        # Check if the dates are updated and state is set to "report"
        report_date_expected = date(2025, 6, 20)
        self.assertEqual(instance.report_date, report_date_expected)
        planned_date_expected = mock_date
        self.assertEqual(instance.planned_date, planned_date_expected)
        self.assertEqual(instance.state, "report")

    def test_new_day_with_non_done_state_and_planned_date_is_past_and_report_date_is_none(self):

        mock_date = date(2025, 6, 24)

        # Create an instance of YourModel with state other than "done"
        instance = TodoFactory(report_date=None, planned_date=date(2025, 6, 20), state="todo")

        # Call the new_day method
        instance.new_day(mock_date)

        # Refresh the instance from the database
        instance.refresh_from_db()

        # Check if the dates are updated and state is set to "report"
        report_date_expected = date(2025, 6, 24)
        self.assertEqual(instance.report_date, report_date_expected)
        planned_date_expected = mock_date
        self.assertEqual(instance.planned_date, planned_date_expected)
        self.assertEqual(instance.state, "report")

    def test_set_done(self):
        mock_date = date(2025, 6, 24)

        # Create an instance of YourModel with state other than "done"
        instance = TodoFactory(planned_date=date(2025, 6, 20), state="todo")

        # Call the new_day method
        instance.set_done(mock_date)

        # Refresh the instance from the database
        instance.refresh_from_db()

        # Check if the dates are updated and state is set to "done"
        self.assertEqual(instance.state, "done")
        self.assertEqual(instance.done_date, mock_date)
