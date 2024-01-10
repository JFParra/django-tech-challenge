from datetime import datetime
from json import loads
from typing import Any, Dict, List

from django.http import HttpRequest, JsonResponse
from django.db.models import CharField, Func, Value

from .models import Quest


# Define a custom Func expression to extract a character at a specific index
class Substr(Func):
    function = "SUBSTR"
    output_field = CharField()


def create_quest(request: HttpRequest) -> JsonResponse:
    post_params: Dict[str, Any] = loads(request.body.decode("utf-8"))
    title: str = post_params.get("title", "")
    description: str = post_params.get("description", "")
    repeats_information: List[bool] = post_params.get("repeats_information", [])

    repeats_on_days: str = (
        "".join(["1" if day else "0" for day in repeats_information])
        if repeats_information
        else None
    )

    quest = Quest(
        title=title,
        description=description,
        completed=False,
        repeats_on_days=repeats_on_days,
    )
    quest.save()

    return JsonResponse({"quest": quest.serialize_as_json()})


def get_quests(request: HttpRequest) -> JsonResponse:
    date_string: str = request.GET.get("date", "")
    date: datetime = datetime.strptime(date_string, "%m-%d-%Y")

    weekday_index = date.weekday() + 1  # 1-based index for SQL

    # General Quests: Not completed and not repeating
    general_quests = Quest.objects.filter(
        date_completed__isnull=True, repeats_on_days__isnull=True
    )

    # Repeating Quests: Match current day of the week and not completed on the date
    repeating_quests = (
        Quest.objects.annotate(repeat_char=Substr("repeats_on_days", weekday_index, 1))
        .filter(repeat_char=Value("1"))
        .exclude(questcompletion__date_completed=date)
    )

    quests = general_quests | repeating_quests

    return JsonResponse({"quests": [quest.serialize_as_json() for quest in quests]})
