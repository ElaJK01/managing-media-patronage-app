from media_patronage.models import Portal, TaskAfterEvent, TaskBeforeEvent, Event


def my_cp(request):
    portals = Portal.objects.all()
    events = Event.objects.all()
    task_after_event = TaskAfterEvent.objects.all()
    task_before_event = TaskBeforeEvent.objects.all()
    category_list = []
    for portal in portals:
        category_list.append(portal.category)
    category_set = list(set(category_list))
    ctx = {
    "portals": portals,
    "task_after_event": task_after_event,
    "task_before_event": task_before_event,
    "events": events,
    "categories": category_set
    }
    return ctx
