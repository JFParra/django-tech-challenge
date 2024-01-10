from typing import Dict

from django.db import models
from django.db.models import Manager


class Quest(models.Model):
    objects = Manager()  # Add this line for mypy type hinting

    id = models.BigAutoField(primary_key=True)
    title = models.TextField(max_length=100)
    description = models.TextField(max_length=150, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True)
    completed = models.BooleanField()
    repeats_on_days = models.CharField(
        max_length=7, null=True
    )  # Represent days as a string, e.g., '0110010'

    def serialize_as_json(self) -> Dict[str, any]:
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "description": self.description,
        }


# Track the completion status of quests on different dates.
class QuestCompletion(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    date_completed = models.DateField()
    completed = models.BooleanField(default=True)

    class Meta:
        unique_together = ("quest", "date_completed")
