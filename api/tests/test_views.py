from datetime import datetime, UTC

from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

from api.models import Quest


class QuestViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def create_quests(self):
        # General Quest - Not completed
        self.general_quest_0 = Quest.objects.create(
            title="General Quest 0",
            description="A one-time general quest 0",
            completed=False,
            date_completed=None,
        )

        # General Quest - Completed
        self.completed_general_quest = Quest.objects.create(
            title="Completed General Quest",
            description="A completed one-time general quest",
            completed=True,
            date_completed=datetime(2021, 2, 15, tzinfo=UTC),
        )

        # Repeating Quest - Repeats on Mondays (index 0)
        self.repeating_quest_0 = Quest.objects.create(
            title="Repeating Quest 0",
            description="A repeating quest 0",
            completed=False,
            repeats_on_days="1000000",  # Repeats on Mondays
        )

        # Repeating Quest - Repeats on M, W, F, Sunday (index 0, 2, 4, 6)
        self.repeating_quest_1 = Quest.objects.create(
            title="Repeating Quest 1",
            description="A repeating quest 1",
            completed=False,
            repeats_on_days="1010101",  # Repeats on M, W, F, Sunday
        )

        # Repeating Quest - Repeats on weekends (indexes 5 - 6)
        self.repeating_quest_2 = Quest.objects.create(
            title="Repeating Quest 2",
            description="A repeating quest 2",
            completed=False,
            repeats_on_days="0000011",  # Repeats on weekends
        )

        # Repeating Quest - Repeats on Sundays (index 6)
        self.completed_repeating_quest = Quest.objects.create(
            title="Completed Repeating Quest",
            description="A completed repeating quest 3",
            completed=True,
            repeats_on_days="0000001",  # Repeats on Sundays
        )

        # Repeating Quest - Repeats everyday
        self.daily_completed_repeating_quest = Quest.objects.create(
            title="Daily Completed Repeating Quest",
            description="A daily completed repeating quest",
            completed=True,
            date_completed=datetime(2021, 2, 14, tzinfo=UTC),  # Sunday
            repeats_on_days="1111111",  # Repeats everyday
        )

    @patch("api.views.datetime")
    def test_general_quests_appearance(self, mock_datetime):
        self.create_quests()

        # Test on any date (general quests should always appear)
        mock_date = datetime(2021, 9, 6)  # Monday
        mock_datetime.strptime.side_effect = lambda *args, **kwargs: datetime.strptime(
            *args, **kwargs
        )
        mock_datetime.now.return_value = mock_date

        response = self.client.get(reverse("get_quests"), {"date": "09-06-2021"})
        data = response.json()

        quest_titles = [quest["title"] for quest in data["quests"]]

        # General Quests should always appear in the get_quests response, until it gets completed.
        self.assertIn("General Quest 0", quest_titles)
        self.assertNotIn("Completed General Quest", quest_titles)

    @patch("api.views.datetime")
    def test_repeating_quests_appearance_on_repeating_day(self, mock_datetime):
        self.create_quests()

        # Test on a repeating day (Monday)
        mock_repeating_day = datetime(2021, 9, 6)  # Monday
        mock_datetime.now.return_value = mock_repeating_day
        mock_datetime.strptime.side_effect = lambda *args, **kwargs: datetime.strptime(
            *args, **kwargs
        )

        response_repeating_day = self.client.get(
            reverse("get_quests"), {"date": "09-06-2021"}
        )
        data_repeating_day = response_repeating_day.json()

        quest_titles = [quest["title"] for quest in data_repeating_day["quests"]]

        # Non completed General Quests and Repeating Quests that have Monday
        self.assertIn("General Quest 0", quest_titles)
        self.assertIn("Repeating Quest 0", quest_titles)
        self.assertIn("Repeating Quest 1", quest_titles)

        # Completed General Quests and Repeating Quests that do not have Monday
        self.assertNotIn("Completed General Quest", quest_titles)
        self.assertNotIn("Repeating Quest 2", quest_titles)
        self.assertNotIn("Completed Repeating Quest", quest_titles)

    @patch("api.views.datetime")
    def test_completed_repeating_quests_appearance_on_repeating_day(
        self, mock_datetime
    ):
        self.create_quests()

        # Test on a repeating day (Monday)
        mock_repeating_day = datetime(2021, 2, 15)  # Monday
        mock_datetime.now.return_value = mock_repeating_day
        mock_datetime.strptime.side_effect = lambda *args, **kwargs: datetime.strptime(
            *args, **kwargs
        )

        response_repeating_day = self.client.get(
            reverse("get_quests"), {"date": "02-15-2021"}
        )
        data_repeating_day = response_repeating_day.json()

        quest_titles = [quest["title"] for quest in data_repeating_day["quests"]]

        # Assert that daily_completed_repeating_quest appears despite it being completed the day before (2-14-2021)
        # Since it appears we can assert and assume that the Quest has not be completed on date requested
        self.assertIn("Daily Completed Repeating Quest", quest_titles)
