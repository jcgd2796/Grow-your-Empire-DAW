from django.shortcuts import render, redirect
from django.template import loader,Context
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as loginAuth, logout as logoutAuth
from DAWActivity.models import Test, Question, TestResolution, Village, Activity,Attack,TradeOffer,Upgrade,Training,Bonus,Student
from datetime import date, timedelta
from django.contrib.auth.models import User as User
from datetime import datetime
# Create your views here.

def rules(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		startDate = date.today()
		endDate= startDate - timedelta(days=3)
		village = Village.objects.filter(owner=request.user)[0]
		activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
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
		return render(request,'DAWActivity/index.html',{'tests':tests})

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

def correctTest(request,testN):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		points = 0
		errors = []
		questions = Question.objects.filter(testName=testN)
		solutions = []
		choices = []
		for x in range (10):
			solutionIndex=(questions[x].correctOption)
			if solutionIndex == 'a':
				solutions.append(questions[x].questionOption1)
			elif solutionIndex == 'b':
				solutions.append(questions[x].questionOption2)
			elif solutionIndex == 'c':
				solutions.append(questions[x].questionOption3)
			else:
				solutions.append(questions[x].questionOption4)
			choices.append(request.POST['select'+str(x)])

		for x in range (10):
			if(solutions[x] == choices[x]):
				points+=1
			else:
				errors.append(x+1)
		if not(TestResolution.objects.filter(testName=testN,userName=request.user).exists()):
			t = TestResolution(testName=Test(testName=testN),userName=request.user,points=points)
			b = Bonus(village=Village.objects.filter(owner = request.user)[0],bonusType=0,bonusAmount=points,completed=0)
			b.save()
			t.save()
			alreadyDone = ''
		else:
			alreadyDone = "Ya has realizado este test. No se han obtenido bonus adicionales"
		if (points == 10):
			text = "No has tenido ningún fallo, ¡Enhorabuena!"
		else:
			text = "Fallo en las preguntas "+str(errors)
		return render(request,'DAWActivity/results.html',{'points':points,'choices':choices,'solutions':solutions,'text':text,'done':alreadyDone})

def manager(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		startDate = date.today()
		endDate= startDate - timedelta(days=7)
		village = Village.objects.filter(owner=request.user)[0]
		activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
		return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities})

def trade(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.filter(owner=request.user)[0]
		villages = Village.objects.exclude(owner=request.user)
		return render(request,'DAWActivity/trade.html',{'village':village,'villages':villages})

def attack(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.filter(owner=request.user)[0]
		villages = Village.objects.exclude(owner=request.user)
		return render(request,'DAWActivity/attack.html',{'villages':villages,'village':village})

def upgrade(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.filter(owner=request.user)[0]
		upgrades = Upgrade.objects.filter(village = village,completed = 0)
		available = [1,2,3,4,5]
		if village.foodLevel == 10:
			available.remove(1)
		if village.woodLevel == 10:
			available.remove(2)
		if village.stoneLevel == 10:
			available.remove(3)
		if village.wallLevel == 10:
			available.remove(4)
		if village.storageLevel == 9:
			available.remove(5)
		for upgrade in upgrades:
			try:
				available.remove(upgrade.building)
			except ValueError: #Already removed
				pass
		return render(request,'DAWActivity/upgrade.html',{'village':village,'upgrades':available})

def train(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.filter(owner=request.user)[0]
		return render(request,'DAWActivity/training.html',{'village':village})

def saveTrade(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		startDate = date.today()
		endDate= startDate - timedelta(days=3)
		seller = Village.objects.filter(owner=request.user)[0]
		buyer = Village.objects.filter(villageName = request.POST['target'])[0]
		wantedRes = [request.POST['wantedWood'],request.POST['wantedStone'],request.POST['wantedFood']]
		offeredRes = [request.POST['offeredWood'],request.POST['offeredStone'],request.POST['offeredFood']]
		if int(offeredRes[0])>seller.storedWood or int(offeredRes[1]) > seller.storedStone or int(offeredRes[2]) > seller.storedFood:
			#not enough resources to trade
			activities = Activity.objects.filter(owner=seller.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
			return render(request,'DAWActivity/manager.html',{'village':seller,'activities':activities,'text':'No tienes recursos suficientes para realizar esta solicitud de comercio'})
		else:
			tradeOffer = TradeOffer(source=seller, destination=buyer,wantedWood=wantedRes[0],wantedStone=wantedRes[1],wantedFood=wantedRes[2],offeredWood=offeredRes[0],offeredStone=offeredRes[1],offeredFood=offeredRes[2],accepted=False)
			tradeOffer.save()
			seller.storedWood-=int(offeredRes[0])
			seller.storedStone-=int(offeredRes[1])
			seller.storedFood-=int(offeredRes[2])
			seller.save()
			activityTrade = Activity(owner=seller,activityText='Has ofrecido un intercambio de recursos a '+buyer.villageName, activityDate=datetime.now())
			activityTrade.save()
			activityTrade = Activity(owner=buyer,activityText=seller.villageName+' Te ofrece un intercambio de recursos.', activityDate=datetime.now())
			activityTrade.save()
			activities = Activity.objects.filter(owner=seller.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
			return render(request,'DAWActivity/manager.html',{'village':seller,'activities':activities,'text':'Solicitud de comercio correctamente creada'})

def saveAttack(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		startDate = date.today()
		endDate= startDate - timedelta(days=3)
		attacker = request.user.username
		defendant = Village.objects.filter(villageName=request.POST['objective'])[0]
		soldiers = request.POST['units']
		village = Village.objects.filter(owner=request.user)[0]
		if int(soldiers) > village.soldiers:
			activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
			#not enough soldiers
			return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'No tienes suficientes soldados para ordenar el ataque solicitado.'})
		else:
			attack = Attack(attacker=village,defendant=defendant,usedSoldiers=soldiers,registeredDateTime=datetime.now(),completed = False)
			attack.save()
			village.soldiers-=int(soldiers)
			village.save()
			attackActivityText='Has ordenado un ataque contra la aldea '+defendant.villageName+' con '+soldiers+' unidades'
			attackActivity = Activity(owner=village,activityText=attackActivityText,activityDate=datetime.now())
			attackActivity.save()
			activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
			return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'Orden de ataque correctamente registrada'})

def saveUpgrade(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.filter(owner=request.user)[0]
		startDate = date.today()
		endDate= startDate - timedelta(days=3)
		building = int(request.POST['selectedIndex'])
		if building == 1: #food
			if village.foodLevel == 10:
				activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
				return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'El edificio ya está al nivel máximo'})
			level = village.foodLevel+1
			woodCost = village.foodLevel * 7
			stoneCost = village.foodLevel * 3

		elif building == 2: #wood
			if village.woodLevel == 10:
				activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
				return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'El edificio ya está al nivel máximo'})
			level = village.woodLevel+1
			woodCost = village.woodLevel * 7
			stoneCost = village.woodLevel * 3

		elif building == 3: #stone
			if village.stoneLevel == 10:
				activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
				return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'El edificio ya está al nivel máximo'})
			level = village.stoneLevel+1
			woodCost = village.stoneLevel * 7
			stoneCost = village.stoneLevel * 3

		elif building == 4: #wall
			if village.wallLevel == 10:
				activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
				return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'El edificio ya está al nivel máximo'})
			level = village.wallLevel+1
			woodCost = village.wallLevel * 5
			stoneCost = village.wallLevel * 10

		elif building == 5: #storage
			if village.storageLevel == 10:
				activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
				return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'El edificio ya está al nivel máximo'})

			level = village.storageLevel+1
			woodCost = village.storageLevel * 3
			stoneCost = village.storageLevel * 2
		completed = False
		if village.storedWood < woodCost or village.storedStone < stoneCost:
			activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
			return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'No tienes recursos necesarios para realizar esta mejora'})
		else:
			upgrades = Upgrade.objects.filter(village = village.villageName,completed = 0)
			for upgrade in upgrades:
				if int(upgrade.building) == int(building):
					activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
					return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'Ya estás mejorando este edificio'})

		village.storedWood-=woodCost
		village.storedStone-=stoneCost
		village.save()
		buildings = ["Granja","Aserradero","Cantera","Muralla","Almacenamiento"]
		upgradeActivityText='Has comenzado a mejorar tu '+buildings[building-1]+' al nivel '+ str(level)
		upgradeActivity = Activity(owner=village,activityText=upgradeActivityText,activityDate=datetime.now())
		upgradeActivity.save()
		up = Upgrade(village=village, level = level,building=building,woodCost = woodCost, stoneCost=stoneCost,completed=False)
		up.save()
		activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
		return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'Actualización creada correctamente'})

def saveTraining(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		startDate = date.today()
		endDate= startDate - timedelta(days=3)
		village = Village.objects.filter(owner=request.user)[0]
		soldiers = int(request.POST['amount'])
		if village.storedFood < int(soldiers)*2:
			activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
			return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'No tienes los recursos necesarios para entrenar la cantidad de soldados especificada'})
		else:
			village.storedFood-=(soldiers*2)
			village.save()
			training = Training(village=village,units=soldiers,foodCost=soldiers*2,completed=False)
			training.save()
			trainActivityText='Has comenzado a entrenar a '+str(soldiers)+' unidad(es)'
			trainActivity = Activity(owner=village,activityText=trainActivityText,activityDate=datetime.now())
			trainActivity.save()
			activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
			return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'Entrenamiento de tropas creado correctamente'})

def manageTrade(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.filter(owner=request.user)[0]
		offersOwned = TradeOffer.objects.filter(source=village,accepted=False)
		offersReceived = TradeOffer.objects.filter(destination=village,accepted=False)
		for offer in offersOwned:
			offer.id=str(hash(str(offer.id)))
		for offer in offersReceived:
			offer.id=str(hash(str(offer.id)))
		return render(request,'DAWActivity/manageTrade.html',{'village':village,'offersOwned':offersOwned,'offersReceived':offersReceived})

def cancelOffer(request,offerHash):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.filter(owner=request.user)[0]
		offersOwned = TradeOffer.objects.filter(source=village,accepted=False)
		for offer in offersOwned:
			if str(hash(str(offer.id))) == offerHash:
				offer.accepted=True
				offer.save()
				activityTrade = Activity(owner=offer.source,activityText='Has cancelado el intercambio de recursos con '+offer.destination.villageName, activityDate=datetime.now())
				activityTrade.save()
				activityTrade = Activity(owner=offer.destination,activityText=offer.source.villageName+' Ha cancelado el intercambio de recursos contigo', activityDate=datetime.now())
				activityTrade.save()
				village.storedWood+=offer.offeredWood
				village.storedStone+=offer.offeredStone
				village.storedFood+=offer.offeredFood
				village.save()
				break;
		startDate = date.today()
		endDate= startDate - timedelta(days=3)
		activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")		
		return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'Oferta cancelada'})

def acceptOffer(request,offerHash):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.filter(owner=request.user)[0]
		offersReceived = TradeOffer.objects.filter(destination=village,accepted=False)
		for offer in offersReceived:
			if str(hash(str(offer.id))) == offerHash:
				if village.storedWood < offer.wantedWood or village.storedStone < offer.wantedStone or village.storedFood<offer.wantedFood:
					activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
					return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'No tienes recursos suficientes para aceptar la oferta'})
				else:
					offer.accepted=True
					offer.save()
					activityTrade = Activity(owner=offer.destination,activityText='Has aceptado el intercambio de recursos con '+offer.destination.villageName, activityDate=datetime.now())
					activityTrade.save()
					activityTrade = Activity(owner=offer.source,activityText=offer.source.villageName+' Ha aceptado el intercambio de recursos contigo', activityDate=datetime.now())
					activityTrade.save()
					village.storedWood-=offer.wantedWood
					village.storedStone-=offer.wantedStone
					village.storedFood-=offer.wantedFood
					village.storedWood+=offer.offeredWood
					village.storedStone+=offer.offeredStone
					village.storedFood+=offer.offeredFood
					village.save()
					source = offer.source
					source.storedWood+=offer.wantedWood
					source.storedStone+=offer.wantedStone
					source.storedFood+=offer.wantedFood
					source.save()
					startDate = date.today()
					endDate= startDate - timedelta(days=3)
					activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")		
					return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'Oferta aceptada'})
		activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
		return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'No se ha encontrado la oferta'})

def rejectOffer(request,offerHash):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.filter(owner=request.user)[0]
		offersReceived = TradeOffer.objects.filter(destination=village,accepted=False)
		for offer in offersReceived:
			if str(hash(str(offer.id))) == offerHash:
				offer.accepted=True
				offer.save()
				activityTrade = Activity(owner=offer.destination,activityText='Has rechazado el intercambio de recursos con '+offer.destination.villageName, activityDate=datetime.now())
				activityTrade.save()
				activityTrade = Activity(owner=offer.source,activityText=offer.source.villageName+' Ha rechazado el intercambio de recursos contigo', activityDate=datetime.now())
				activityTrade.save()
				source = offer.source
				source.storedWood+=offer.offeredWood
				source.storedStone+=offer.offeredStone
				source.storedFood+=offer.offeredFood
				source.save()
				startDate = date.today()
				endDate= startDate - timedelta(days=3)
				activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")		
				return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'Oferta aceptada'})
		activities = Activity.objects.filter(owner=village.villageName,activityDate__range=[endDate,startDate]).order_by("-activityDate")
		return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'No se ha encontrado la oferta'})



