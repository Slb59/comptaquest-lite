"""Tests for diarylab.models"""

from django.test import TransactionTestCase
from django.utils import timezone

from diarylab.models import DiaryEntry
from tests.factories.diarylab import DiaryEntryFactory
from tests.factories.member import MemberFactory


class TestDiaryEntry(TransactionTestCase):
    def setUp(self):
        self.user = MemberFactory()
        self.diary_entry = DiaryEntryFactory(user=self.user)

    def test_diary_entry_creation(self):
        """Test that a diary entry can be created successfully"""
        self.assertEqual(DiaryEntry.objects.count(), 1)
        self.assertEqual(self.diary_entry.user, self.user)

    def test_string_representation(self):
        """Test that the string representation is correct"""
        expected_str = f"Entry from {self.diary_entry.date}"
        self.assertEqual(str(self.diary_entry), expected_str)

    def test_date_ordering(self):
        """Test that diary entries are ordered by date"""

        # delete the entry created in setUp
        DiaryEntry.objects.filter(user=self.user).delete()

        # Create another entry with a different date
        now_entry = DiaryEntryFactory(user=self.user, date=timezone.now().date())
        older_entry = DiaryEntryFactory(
            user=self.user, date=(timezone.now() - timezone.timedelta(days=2)).date()
        )
        newer_entry = DiaryEntryFactory(
            user=self.user, date=(timezone.now() + timezone.timedelta(days=1)).date()
        )

        entries = DiaryEntry.objects.all()
        self.assertEqual(entries[0].date, older_entry.date)
        self.assertEqual(entries[1].date, now_entry.date)
        self.assertEqual(entries[2].date, newer_entry.date)

    def test_user_relationship(self):
        """Test that diary entries are properly related to users"""
        # Create another user and entry
        other_user = MemberFactory()
        other_entry = DiaryEntryFactory(user=other_user)  # noqa: F841

        # Test that entries are filtered by user correctly
        user_entries = DiaryEntry.objects.filter(user=self.user)
        self.assertEqual(user_entries.count(), 1)
        self.assertEqual(user_entries.first(), self.diary_entry)

    def test_content_validation(self):
        """Test that content can be empty but must be a string"""
        # Test empty content
        empty_entry = DiaryEntryFactory(content="")
        self.assertEqual(empty_entry.content, "")

        # Test long content
        long_content = "a" * 1000
        long_entry = DiaryEntryFactory(content=long_content)
        self.assertEqual(long_entry.content, long_content)

    def test_date_default(self):
        """Test that date defaults to current date"""
        entry = DiaryEntry()
        self.assertLessEqual(timezone.now() - entry.date, timezone.timedelta(minutes=1))

    def test_auto_timestamps(self):
        """Test that created_at and updated_at timestamps work correctly"""
        entry = DiaryEntryFactory()

        # Test created_at
        self.assertLessEqual(
            timezone.now() - entry.created_at, timezone.timedelta(minutes=1)
        )

        # Test that updated_at is set
        self.assertIsNotNone(entry.updated_at)

        # Test that updated_at changes on save
        original_updated_at = entry.updated_at
        entry.content = "New content"
        entry.save()
        self.assertNotEqual(entry.updated_at, original_updated_at)
        self.assertLessEqual(
            timezone.now() - entry.updated_at, timezone.timedelta(minutes=1)
        )
