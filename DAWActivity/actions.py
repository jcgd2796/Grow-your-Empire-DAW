from datetime import timedelta
from django.utils import timezone
from DAWActivity.models import Bonus, Training, Upgrade, Village, Activity, Attack

def processUpgrades():
	upgrades = Upgrade.objects.filter(completed=False)
	for upgrade in upgrades:
		village = Village.objects.get(owner = upgrade.village)
		if upgrade.building == 1: #food
			village.foodLevel += 1
			village.dailyFood = round(village.dailyFood*1.1)
			village.save()
			Activity(activityText='Ha finalizado la mejora de tu granja al nivel '+ str(village.foodLevel),activityDate=timezone.now(),owner=village).save()
		elif upgrade.building == 2: #wood
			village.woodLevel += 1
			village.dailyWood = round(village.dailyWood*1.1)
			village.save()
			Activity(activityText='Ha finalizado la mejora de tu aserradero al nivel '+ str(village.woodLevel),activityDate=timezone.now(),owner=village).save()
		elif upgrade.building == 3: #stone
			village.stoneLevel += 1
			village.dailyStone = round(village.dailyStone*1.1)
			village.save()
			Activity(activityText='Ha finalizado la mejora de tu cantera al nivel '+ str(village.stoneLevel),activityDate=timezone.now(),owner=village).save()
		elif upgrade.building == 4: #wall
			village.wallLevel += 1
			village.save()
			Activity(activityText='Ha finalizado la mejora de tu muralla al nivel '+ str(village.wallLevel),activityDate=timezone.now(),owner=village).save()
		elif upgrade.building == 5: #storage
			village.storageLevel += 1
			village.save()
			Activity(activityText='Ha finalizado la mejora de tu almacén al nivel '+ str(village.storageLevel),activityDate=timezone.now(),owner=village).save()
		upgrade.completed=True
		upgrade.save()
	return True

def processTraining():
	trainings = Training.objects.filter(completed=False)
	for training in trainings:
		village = Village.objects.get(owner=training.village)
		village.soldiers += training.units
		village.save()
		Activity(activityText='Ha finalizado el entrenamiento de '+ str(training.units)+' unidad(es)',activityDate=timezone.now(),owner=village).save()
		training.completed = True;
		training.save()
	return True
	
def processAttack():
	attacks = Attack.objects.filter(completed=False)
	for attack in attacks:
		attacker = Village.objects.get(owner = attack.attacker)
		defendant = Village.objects.get(owner = attack.defendant)
		defendant_virtualUnits = round(defendant.soldiers*(1+0.1*defendant.wallLevel))
		if attack.usedSoldiers > defendant_virtualUnits: #attacker wins
			availableResources = [
				round(defendant.storedFood*(1-0.1*defendant.storageLevel)),
				round(defendant.storedWood*(1-0.1*defendant.storageLevel)),
				round(defendant.storedStone*(1-0.1*defendant.storageLevel))]
			Activity(
				activityText=str(attacker.villageName)+' te ha atacado. Has perdido '+str(defendant.soldiers)+' soldados y te han saqueado '+str(availableResources[0])+' de alimento, '+str(availableResources[1])+' de madera y '+str(availableResources[2])+' de piedra'
				,activityDate=timezone.now(),owner=defendant).save()
			Activity(
				activityText='Has atacado a '+str(defendant.villageName)+' y has ganado. Han vuelto '+str(round(attack.usedSoldiers-defendant_virtualUnits))+' soldados y has saqueado '+str(availableResources[0])+' de alimento, '+str(availableResources[1])+' de madera y '+str(availableResources[2])+' de piedra'
				,activityDate=timezone.now(),owner=attacker).save()
			defendant.soldiers = 0
			defendant.storedFood -= availableResources[0]
			defendant.storedWood -= availableResources[1]
			defendant.storedStone -= availableResources[2]
			defendant.save()
			attacker.soldiers += (attack.usedSoldiers-defendant_virtualUnits)
			attacker.storedFood += availableResources[0]
			attacker.storedWood += availableResources[1]
			attacker.storedStone += availableResources[2]
			attacker.save()
		else: #defendant wins
			if defendant_virtualUnits - attack.usedSoldiers > defendant.soldiers: #defendant lost no soldiers
				Activity(
				activityText=attacker.villageName+' te ha atacado. Tus soldados han repelido el ataque. No has perdido soldados ni recursos'
				,activityDate=timezone.now(),owner=defendant).save()
			else:
				lostSoldiers = defendant.soldiers - (defendant_virtualUnits - attack.usedSoldiers)
				Activity(
				activityText=attacker.villageName+' te ha atacado. Tus soldados han repelido el ataque. Has perdido '+str(lostSoldiers)+' soldados, pero no has perdido recursos'
				,activityDate=timezone.now(),owner=defendant).save()
				defendant.soldiers-=lostSoldiers
				defendant.save()
			Activity(
				activityText='Has atacado a '+defendant.villageName+'. Sus soldados han repelido el ataque. Has perdido los '+str(attack.usedSoldiers)+' soldados empleados en el ataque'
				,activityDate=timezone.now(),owner=attacker).save()
		attack.completed = True
		attack.save()	
	return True
	
def addResources():
	villages = Village.objects.filter(disabled = False)
	for village in villages:
		bonuses = Bonus.objects.filter(village = village, completed = False, bonusType = 0)
		totalMultiplier = 1.0
		for bonus in bonuses:
			totalMultiplier+=(bonus.bonusAmount/10)
			bonus.completed = True
			bonus.save()
		village.storedFood += village.dailyFood*totalMultiplier
		village.storedWood += village.dailyWood*totalMultiplier
		village.storedStone += village.dailyStone*totalMultiplier
		village.save()
	return True

def processBonuses():
	bonuses = Bonus.objects.filter(completed = False).exclude(bonusType = 0)
	for bonus in bonuses:
		village = Village.objects.get(owner = bonus.village)
		if bonus.bonusType == 1: #units
			village.soldiers += bonus.bonusAmount
		elif bonus.bonusType == 2: #building
			if bonus.bonusAmount == 0: #food
				village.foodLevel += 1
			elif bonus.bonusAmount == 1: #wood
				village.woodLevel += 1
			elif bonus.bonusAmount == 2: #stone
				village.stoneLevel += 1
			elif bonus.bonusAmount == 3: #walls
				village.wallLevel += 1
			elif bonus.bonusAmount == 4: #storage
				village.storageLevel += 1
		village.save()
		bonus.completed = True
		bonus.save()
	return True

def disableVillages():
	startDate = timezone.now()
	endDate = startDate - timedelta(days=3)
	villages = Village.objects.filter(lastLogin__lt = endDate)
	for village in villages:
		village.disabled = True
		village.save()
	return True

def main():
		disableVillages()
		processBonuses()
		processUpgrades()
		processTraining()
		processAttack()
		addResources()

if __name__ == "__main__":
    main()
