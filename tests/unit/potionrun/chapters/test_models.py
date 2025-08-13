# tests/unit/potionrun/chapters/test_models.py
from django.core.exceptions import ValidationError
from django.test import TestCase

from potionrun.chapters.models import Act, Chapter, Scene


class ChapterModelTest(TestCase):
    def setUp(self):
        self.chapter = Chapter.objects.create(
            name="5km - 30mn", description="Objectif 5km en 30 minutes"
        )

    def test_chapter_creation(self):
        self.assertEqual(self.chapter.name, "5km - 30mn")
        self.assertEqual(self.chapter.completed_sessions, 0)
        self.assertEqual(self.chapter.associated_routes, 0)

    def test_chapter_str(self):
        self.assertEqual(str(self.chapter), "5km - 30mn")


class ActModelTest(TestCase):
    def setUp(self):
        self.chapter = Chapter.objects.create(name="Test")
        self.act = Act.objects.create(
            chapter=self.chapter, number=1, short="Acte I", description="Premier acte"
        )

    def test_act_creation(self):
        self.assertEqual(self.act.number, 1)
        self.assertEqual(self.act.short, "Acte I")
        self.assertEqual(str(self.act), "Acte 1 - Acte I")

    def test_act_choices(self):
        choices = [(i, f"Acte {i}") for i in range(1, 8)]
        self.assertIn((1, "Acte 1"), choices)

    def test_act_number_validation(self):
        with self.assertRaises(ValidationError):
            Act.objects.create(
                chapter=self.chapter, number=8, short="Acte VIII"
            )  # Invalide (doit être entre 1 et 7)

    def test_chapter_act_relation(self):
        self.assertEqual(self.chapter.acts.count(), 1)
        self.assertEqual(self.act.chapter, self.chapter)


class SceneModelTest(TestCase):
    def setUp(self):
        self.chapter = Chapter.objects.create(name="Test")
        self.act = Act.objects.create(chapter=self.chapter, number=1)
        self.scene = Scene.objects.create(
            act=self.act,
            number=1,
            short="Scène 1",
            instructions="=> Instruction 1\n=> Instruction 2",
        )

    def test_scene_creation(self):
        self.assertEqual(self.scene.number, 1)
        self.assertEqual(self.scene.short, "Scène 1")

    def test_scene_instructions(self):
        instructions = self.scene.get_instructions_list()
        self.assertEqual(instructions, ["Instruction 1", "Instruction 2"])

    def test_scene_str(self):
        self.assertEqual(str(self.scene), "Scène 1 - Scène 1")

    def test_scene_instructions_empty(self):
        scene = Scene.objects.create(act=self.act, number=2, instructions="")
        self.assertEqual(scene.get_instructions_list(), [])
