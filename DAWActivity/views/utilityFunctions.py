from datetime import date, timedelta

from DAWActivity.models import Activity, Village

def getActivities(user):
    startDate = date.today()
    endDate = startDate - timedelta(days=3)
    return Activity.objects.filter(owner=user,activityDate__range=[endDate,startDate]).order_by("-activityDate")

def updateVillage(name):
    village = Village.objects.filter(villageName= name)[0]
    village.lastLogin=date.today()
    village.disabled=False
    village.save()