from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration


def format_duration(delta):
    duration = f"{delta // 3600} ч : {delta % 3600 // 60} мин : {delta % 3600 % 60} сек"
    return duration


def storage_information_view(request):
    not_leave_passcards = Visit.objects.filter(leaved_at=None).select_related(
        "passcard"
    )
    non_closed_visits = []
    for not_leave_passcard in not_leave_passcards:
        non_closed_visits.append(
            {
                "who_entered": not_leave_passcard.passcard.owner_name,
                "entered_at": not_leave_passcard.entered_at,
                "duration": format_duration(
                    get_duration(not_leave_passcard.entered_at)
                ),
            }
        )
    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, "storage_information.html", context)