from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as loginAuth, logout as logoutAuth
from DAWActivity.models import Test,Question,Village,Student,New
from datetime import date
from django.contrib.auth.models import User as User

from DAWActivity.views import utilityFunctions

def rules(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.filter(owner=request.user)[0]
		activities = utilityFunctions.getActivities(village.villageName)
		return render(request,'DAWActivity/rules.html',{'village':village,'activities':activities})

def ranking(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		villages = Village.objects.all()
		villagesDict = {}
		for village in villages:
			punt = 0;
			punt += village.storedFood + village.storedWood + village.storedStone + 10*(village.foodLevel+village.woodLevel+village.stoneLevel+village.wallLevel+village.storageLevel)+(2*village.soldiers)
			villagesDict[village.villageName]=punt
		sorteddict = dict(sorted(villagesDict.items(),key=lambda x:x[1],reverse=True)[:5])
	return render(request,'DAWActivity/ranking.html',{'ranking':sorteddict})

def index(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		if Student.objects.filter(user_id=request.user.id)[0].subject == 3: #admin
			tests = Test.objects.all()
		else:
			tests = Test.objects.filter(subject = Student.objects.filter(user_id=request.user.id)[0].subject)
		news = New.objects.all().order_by("-newDate")	
		return render(request,'DAWActivity/index.html',{'tests':tests,'news':news})

def login(request):
	usr = request.POST['user']
	pas = request.POST['password']
	user = authenticate(request,username=usr,password = pas)
	if user is not None:
		loginAuth(request,user)
		return redirect('index')
	else:
		return render(request,'DAWActivity/login.html',{'msg':'Usuario o contraseña incorrectos.'})

def logout(request):
	logoutAuth(request)
	return render(request,'DAWActivity/login.html',{'msg':'Sesión finalizada correctamente'})

def test(request,testN):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		t = Test.objects.filter(testName=testN)[0]
		questions = Question.objects.filter(testName=t)
		qs = []
		opts = []
		for x in range(10):
			qs.append(questions[x].questionText)
			opts.append([])
			opts[x].append(questions[x].questionOption1)
			opts[x].append(questions[x].questionOption2)
			opts[x].append(questions[x].questionOption3)
			opts[x].append(questions[x].questionOption4)
		return render(request,'DAWActivity/test.html',{'test':testN,'questions':qs,'options0':opts[0],'options1':opts[1],'options2':opts[2],'options3':opts[3],'options4':opts[4],'options5':opts[5],'options6':opts[6],'options7':opts[7],'options8':opts[8],'options9':opts[9]})

def manager(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.filter(owner=request.user)[0]
		utilityFunctions.updateVillage(village.villageName)
		activities = utilityFunctions.getActivities(village.villageName)
		return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities})

def news(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		news = New.objects.all().order_by("-newDate")
		return render(request,'DAWActivity/news.html',{'news':news})

def new (request,newTitle):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		new = New.objects.filter(title=newTitle)	
		return render(request,'DAWActivity/new.html',{'news':new})

