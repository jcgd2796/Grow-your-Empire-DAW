from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('login',views.login,name='Login'),
        path('logout',views.logout,name='Logout'),
        path('test<str:testN>/',views.test,name='Test'),
	path('test<str:testN>/correct',views.correctTest,name='Test resolution'),
	path('rules',views.rules,name='Rules'),
	path('ranking',views.ranking,name='Ranking'),
	path('manager',views.manager,name='Manager'),
	path('manager/trade',views.trade,name='Trade'),
	path('manager/attack',views.attack,name='Attack'),
	path('manager/upgrade',views.upgrade,name='Upgrade'),
	path('manager/train',views.train,name='Training'),
	path('manager/saveTrade',views.saveTrade,name='Save trade'),
	path('manager/saveAttack',views.saveAttack,name='Save attack'),
	path('manager/saveUpgrade',views.saveUpgrade,name='Save upgrade'),
	path('manager/saveTraining',views.saveTraining,name='Save training'),
	path('manager/manageOffers',views.manageTrade,name='Manage offers'),
	path('manager/cancelOffer<str:offerHash>/',views.cancelOffer,name='Cancel offer'),
	path('manager/acceptOffer<str:offerHash>/',views.acceptOffer,name='Cancel offer'),
	path('manager/RejectOffer<str:offerHash>/',views.rejectOffer,name='Cancel offer'),
]
