from django.test import TestCase

from api.models import Quest


class QuestModelTests(TestCase):
    def test_create_non_repeating_quest(self):
        quest = Quest.objects.create(
            title="Non-Repeating Quest", description="A one-time quest", completed=False
        )
        self.assertIsNone(quest.repeats_on_days)

    def test_create_repeating_quest(self):
        repeating_pattern = "1010100"  # e.g., repeat on Monday, Wednesday, Friday
        quest = Quest.objects.create(
            title="Repeating Quest",
            description="A repeating quest",
            completed=False,
            repeats_on_days=repeating_pattern,
        )
        self.assertEqual(quest.repeats_on_days, repeating_pattern)

    def test_serialize_as_json(self):
        quest = Quest.objects.create(
            title="Sample Quest", description="A simple quest", completed=False
        )
        serialized_data = quest.serialize_as_json()
        self.assertEqual(serialized_data["title"], quest.title)
        self.assertEqual(serialized_data["description"], quest.description)
        self.assertEqual(serialized_data["completed"], quest.completed)
