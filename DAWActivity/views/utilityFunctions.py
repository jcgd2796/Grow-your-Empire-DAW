from datetime import date, timedelta

from DAWActivity.models import Activity, Village

def getActivities(user):
    startDate = date.today()
    endDate = startDate - timedelta(days=3)
    return Activity.objects.filter(owner=user,activityDate__range=[endDate,startDate]).order_by("-activityDate")

def updateVillage(name):
    village = Village.objects.get(villageName= name)
    village.lastLogin=date.today()
    village.disabled=False
    village.save()