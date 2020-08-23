from media_patronage.models import Portal

def my_cp(request):
    portals = Portal.objects.all()
    ctx = {
    "portals": portals,

    }
    return ctx
