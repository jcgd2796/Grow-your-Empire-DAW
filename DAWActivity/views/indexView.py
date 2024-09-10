from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.utils import timezone
from django.contrib.auth import login as loginAuth, logout as logoutAuth
from DAWActivity.models import Test,Question, Option,Village,Student,New
from django.contrib.auth.models import User as User

from DAWActivity.database import utilityFunctions

def rules(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		return render(request,'DAWActivity/rules.html')

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
		if request.user.is_superuser:
			tests = Test.objects.all()
		else:
			tests = Test.objects.filter(subject__in=list(request.user.student.subject.all()), date__lt = timezone.now())
		news = New.objects.all().order_by("-registeredDateTime")	
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
		t = Test.objects.get(testName=testN)
		questions = list(Question.objects.filter(testName=t))
		questionOpts = []
		for question in questions:
			if question.questionType == "Opciones":
				questionOpts.extend(Option.objects.filter(questionText = question))
		return render(request,'DAWActivity/test.html',{'questions':questions,'questionOpts':questionOpts})

def manager(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.get(owner = request.user.student)
		utilityFunctions.updateVillage(village.villageName)
		activities = utilityFunctions.getActivities(village)
		return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities})

def news(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		news = New.objects.all().order_by("-registeredDateTime")
		return render(request,'DAWActivity/news.html',{'news':news})

def new (request,newTitle):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		new = New.objects.filter(title=newTitle)	
		return render(request,'DAWActivity/new.html',{'news':new})

