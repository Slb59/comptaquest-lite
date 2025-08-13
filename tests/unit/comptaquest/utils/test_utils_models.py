from django.core.exceptions import ValidationError
from django.test import TestCase

from comptaquest.utils.models import Codification, File, Parameter
from tests.factories.codification import PaymentCodificationFactory
from tests.factories.member import MemberFactory


class TestModelCodification(TestCase):

    def setUp(self):
        self.codification = PaymentCodificationFactory(
            name="Test Codification", description="A test description"
        )

    def test_codification_creation(self):
        self.assertEqual(self.codification.name, "Test Codification")
        self.assertEqual(self.codification.description, "A test description")
        self.assertEqual(self.codification.state, Codification.CodeStatus.ACTIF)
        self.assertEqual(self.codification.codetype, Codification.CodeType.PAYMENT)

    def test_codification_invalid_state(self):
        self.codification.state = "Invalid"
        with self.assertRaises(ValidationError):
            self.codification.full_clean()  # Validates choices

    def test_codification_related_user(self):
        self.assertEqual(str(self.codification.user), "MB1")


class TestModelFile(TestCase):
    def setUp(self):
        self.user = MemberFactory()
        self.user.save()
        self.file = File.objects.create(
            user=self.user,
            name="Test File",
            description="A test file description",
            path="/path/to/testfile",
        )

    def test_file_creation(self):
        self.assertEqual(self.file.name, "Test File")
        self.assertEqual(self.file.description, "A test file description")
        self.assertEqual(self.file.path, "/path/to/testfile")

    def test_file_related_user(self):
        self.assertEqual(self.file.user, self.user)


class TestModelParameter(TestCase):
    def setUp(self):
        self.user = MemberFactory()
        self.user.save()
        self.parameter = Parameter.objects.create(
            user=self.user,
            name="Test Parameter",
            description="A test parameter description",
            value="Test Value",
        )

    def test_parameter_creation(self):
        self.assertEqual(self.parameter.name, "Test Parameter")
        self.assertEqual(self.parameter.description, "A test parameter description")
        self.assertEqual(self.parameter.value, "Test Value")

    def test_parameter_related_user(self):
        self.assertEqual(self.parameter.user, self.user)
