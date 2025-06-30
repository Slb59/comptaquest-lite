from django.test import TestCase

from tests.factories.sami import SamiFactory


class SamiModelTest(TestCase):
    def setUp(self):
        self.sami = SamiFactory()

    def test_sami_str(self):
        self.assertEqual(str(self.sami), f"Sami data {self.sami.date}")

    def test_total_sleep(self):
        expected = sum(
            [
                self.sami.bedtime,
                self.sami.wakeup,
                self.sami.nonstop,
                self.sami.energy,
                self.sami.naptime,
                self.sami.phone,
                self.sami.reading,
            ]
        )
        self.assertEqual(self.sami.total_sleep, expected)

    def test_total_food(self):
        expected = sum(
            [
                self.sami.fruits,
                self.sami.vegetables,
                self.sami.meals,
                self.sami.desserts,
                self.sami.sugardrinks,
                self.sami.nosugardrinks,
            ]
        )
        self.assertEqual(self.sami.total_food, expected)

    def test_total_move(self):
        expected = sum(
            [
                self.sami.homework,
                self.sami.garden,
                self.sami.Outsidetime,
                self.sami.endurancesport,
                self.sami.yogasport,
            ]
        )
        self.assertEqual(self.sami.total_move, expected)

    def test_total_idea(self):
        expected = sum(
            [
                self.sami.computer,
                self.sami.youtube,
                self.sami.administrative,
                self.sami.papergames,
                self.sami.videogames,
            ]
        )
        self.assertEqual(self.sami.total_idea, expected)

    def test_total_sami(self):
        expected = self.sami.total_sleep + self.sami.total_food + self.sami.total_move + self.sami.total_idea
        self.assertEqual(self.sami.total_sami, expected)

    def test_field_validators_boundaries(self):
        """Test that we can create an instance with the minimum and maximum values allowed"""
        sami_min = SamiFactory(
            weight=0,
            bedtime=0,
            wakeup=0,
            nonstop=0,
            energy=0,
            naptime=0,
            phone=0,
            reading=0,
            fruits=0,
            vegetables=0,
            meals=0,
            desserts=0,
            sugardrinks=0,
            nosugardrinks=0,
            homework=0,
            garden=0,
            Outsidetime=0,
            endurancesport=0,
            yogasport=0,
            videogames=0,
            papergames=0,
            administrative=0,
            computer=0,
            youtube=0,
        )
        self.assertEqual(sami_min.total_sami, 0)

        sami_max = SamiFactory(
            weight=0,
            bedtime=3,
            wakeup=3,
            nonstop=5,
            energy=5,
            naptime=4,
            phone=2,
            reading=3,
            fruits=3,
            vegetables=2,
            meals=5,
            desserts=5,
            sugardrinks=5,
            nosugardrinks=5,
            homework=5,
            garden=5,
            Outsidetime=5,
            endurancesport=5,
            yogasport=5,
            videogames=5,
            papergames=5,
            administrative=5,
            computer=5,
            youtube=5,
        )
        self.assertEqual(sami_max.total_sami, 100)
