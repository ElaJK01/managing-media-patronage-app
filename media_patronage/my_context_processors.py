from media_patronage.models import Portal, TaskAfterEvent, TaskBeforeEvent, Event


def my_cp(request):
    portals = Portal.objects.all()
    events = Event.objects.all()
    task_after_event = TaskAfterEvent.objects.all()
    task_before_event = TaskBeforeEvent.objects.all()
    ctx = {
    "portals": portals,
    "task_after_event": task_after_event,
    "task_before_event": task_before_event,
    "events": events,

    }
    return ctx
