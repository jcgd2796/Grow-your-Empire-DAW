from datetime import datetime
from django.shortcuts import render

from DAWActivity.views import utilityFunctions
from DAWActivity.models import TradeOffer, Training, Upgrade, Village, Activity, Attack

def saveAttack(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		defendant = Village.objects.get(villageName=request.POST['objective'])
		soldiers = request.POST['units']
		village = Village.objects.get(owner=request.user)
		if int(soldiers) > village.soldiers:
			activities = utilityFunctions.getActivities(village.villageName)
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
			activities = utilityFunctions.getActivities(village.villageName)
			return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'Orden de ataque correctamente registrada'})
		
def trade(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.get(owner=request.user)
		villages = Village.objects.exclude(owner=request.user)
		return render(request,'DAWActivity/trade.html',{'village':village,'villages':villages})

def attack(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.get(owner=request.user)
		villages = Village.objects.exclude(owner=request.user)
		return render(request,'DAWActivity/attack.html',{'villages':villages,'village':village})

def upgrade(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.get(owner=request.user)
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
		village = Village.objects.get(owner=request.user)
		return render(request,'DAWActivity/training.html',{'village':village})

def saveTrade(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		seller = Village.objects.get(owner=request.user)
		buyer = Village.objects.get(villageName = request.POST['target'])
		wantedRes = [request.POST['wantedWood'],request.POST['wantedStone'],request.POST['wantedFood']]
		offeredRes = [request.POST['offeredWood'],request.POST['offeredStone'],request.POST['offeredFood']]
		if int(offeredRes[0])>seller.storedWood or int(offeredRes[1]) > seller.storedStone or int(offeredRes[2]) > seller.storedFood:
			#not enough resources to trade
			activities = utilityFunctions.getActivities(seller.villageName)
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
			activities = utilityFunctions.getActivities(seller.villageName)
			return render(request,'DAWActivity/manager.html',{'village':seller,'activities':activities,'text':'Solicitud de comercio correctamente creada'})

def saveUpgrade(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.get(owner=request.user)
		building = int(request.POST['selectedIndex'])
		activities = utilityFunctions.getActivities(village.villageName)
		if building == 1: #food
			if village.foodLevel == 10:
				return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'El edificio ya está al nivel máximo'})
			level = village.foodLevel+1
			woodCost = village.foodLevel * 7
			stoneCost = village.foodLevel * 3

		elif building == 2: #wood
			if village.woodLevel == 10:
				return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'El edificio ya está al nivel máximo'})
			level = village.woodLevel+1
			woodCost = village.woodLevel * 7
			stoneCost = village.woodLevel * 3

		elif building == 3: #stone
			if village.stoneLevel == 10:
				return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'El edificio ya está al nivel máximo'})
			level = village.stoneLevel+1
			woodCost = village.stoneLevel * 7
			stoneCost = village.stoneLevel * 3

		elif building == 4: #wall
			if village.wallLevel == 10:
				return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'El edificio ya está al nivel máximo'})
			level = village.wallLevel+1
			woodCost = village.wallLevel * 5
			stoneCost = village.wallLevel * 10

		elif building == 5: #storage
			if village.storageLevel == 10:
				return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'El edificio ya está al nivel máximo'})

			level = village.storageLevel+1
			woodCost = village.storageLevel * 3
			stoneCost = village.storageLevel * 2
		completed = False
		if village.storedWood < woodCost or village.storedStone < stoneCost:
			return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'No tienes recursos necesarios para realizar esta mejora'})
		else:
			upgrades = Upgrade.objects.filter(village = village.villageName,completed = 0)
			for upgrade in upgrades:
				if int(upgrade.building) == int(building):
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
		activities = utilityFunctions.getActivities(village.villageName)
		return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'Actualización creada correctamente'})

def saveTraining(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.get(owner=request.user)
		soldiers = int(request.POST['amount'])
		if village.storedFood < int(soldiers)*2:
			activities = utilityFunctions.getActivities(village.villageName)
			return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'No tienes los recursos necesarios para entrenar la cantidad de soldados especificada'})
		else:
			village.storedFood-=(soldiers*2)
			village.save()
			training = Training(village=village,units=soldiers,foodCost=soldiers*2,completed=False)
			training.save()
			trainActivityText='Has comenzado a entrenar a '+str(soldiers)+' unidad(es)'
			trainActivity = Activity(owner=village,activityText=trainActivityText,activityDate=datetime.now())
			trainActivity.save()
			activities = utilityFunctions.getActivities(village.villageName)
			return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'Entrenamiento de tropas creado correctamente'})

def manageTrade(request):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.get(owner=request.user)
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
		village = Village.objects.get(owner=request.user)
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
		activities = utilityFunctions.getActivities(village.villageName)
		return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'Oferta cancelada'})

def acceptOffer(request,offerHash):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.get(owner=request.user)
		offersReceived = TradeOffer.objects.filter(destination=village,accepted=False)
		for offer in offersReceived:
			if str(hash(str(offer.id))) == offerHash:
				if village.storedWood < offer.wantedWood or village.storedStone < offer.wantedStone or village.storedFood<offer.wantedFood:
					activities = utilityFunctions.getActivities(village.villageName)
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
					activities = utilityFunctions.getActivities(village.villageName)		
					return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'Oferta aceptada'})
		activities = utilityFunctions.getActivities(village.villageName)
		return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'No se ha encontrado la oferta'})

def rejectOffer(request,offerHash):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		village = Village.objects.get(owner=request.user)
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
				activities = utilityFunctions.getActivities(village.villageName)
				return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'Oferta aceptada'})
		activities = utilityFunctions.getActivities(village.villageName)
		return render(request,'DAWActivity/manager.html',{'village':village,'activities':activities,'text':'No se ha encontrado la oferta'})