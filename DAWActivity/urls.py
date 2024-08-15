from django.urls import path
from DAWActivity.views import indexView, villageView, testView

urlpatterns = [
	path('', indexView.index, name='index'),
	path('login',indexView.login,name='Login'),
    path('logout',indexView.logout,name='Logout'),
    path('test<str:testN>/',indexView.test,name='Test'),
	path('test<str:testN>/correct',testView.correctTest,name='Test resolution'),
	path('rules',indexView.rules,name='Rules'),
	path('ranking',indexView.ranking,name='Ranking'),
    path('news',indexView.news,name='News'),
    path('new<str:newTitle>',indexView.new,name='New'),
	path('manager',indexView.manager,name='Manager'),
	path('manager/trade',villageView.trade,name='Trade'),
	path('manager/attack',villageView.attack,name='Attack'),
	path('manager/upgrade',villageView.upgrade,name='Upgrade'),
	path('manager/train',villageView.train,name='Training'),
	path('manager/saveTrade',villageView.saveTrade,name='Save trade'),
	path('manager/saveAttack',villageView.saveAttack,name='Save attack'),
	path('manager/saveUpgrade',villageView.saveUpgrade,name='Save upgrade'),
	path('manager/saveTraining',villageView.saveTraining,name='Save training'),
	path('manager/manageOffers',villageView.manageTrade,name='Manage offers'),
	path('manager/cancelOffer<str:offerHash>/',villageView.cancelOffer,name='Cancel offer'),
	path('manager/acceptOffer<str:offerHash>/',villageView.acceptOffer,name='Accept offer'),
	path('manager/RejectOffer<str:offerHash>/',villageView.rejectOffer,name='Reject offer'),
]
