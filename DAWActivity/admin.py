from django.contrib import admin
from .models import Test, Option, Question, TestResolution, Village, Activity, Attack, TradeOffer,New, Upgrade, Training, Bonus,Student
# Register your models here.
admin.site.register(Test)
admin.site.register(TestResolution)
admin.site.register(Village)
admin.site.register(Activity)
admin.site.register(Attack)
admin.site.register(TradeOffer)
admin.site.register(Upgrade)
admin.site.register(Training)
admin.site.register(Bonus)
admin.site.register(Student)
admin.site.register(New)
admin.site.register(Question)
admin.site.register(Option)
