import sqlite3

def processUpgrades():
	#/home/pi/Documents/Django/TFM/db.sqlite3
	connection = sqlite3.connect('/home/jcgd/Documents/Grow_your_empire/DAWActivity/db.sqlite3')
	cursor = connection.cursor()
	upgrades = cursor.execute('SELECT id,building,village_id FROM dawactivity_upgrade WHERE completed = 0').fetchall()
	#[id,building,village]
	for upgrade in upgrades:
		#[name, daily food, daily wood, daily stone, food level, wood level, stone level, walls level, storage level]
		village = cursor.execute("SELECT villageName,dailyFood,dailyWood,dailyStone,foodLevel,woodLevel,stoneLevel,wallLevel,storageLevel FROM dawactivity_village WHERE villageName = '"+str(upgrade[2])+"'").fetchone()
		if village != None:
			if upgrade[1] == 1: #food
				level = village[4]+1
				dailyFood = round(village[1]*1.1)
				cursor.execute("UPDATE dawactivity_village SET foodLevel = "+str(level)+", dailyFood = "+str(dailyFood)+" WHERE villageName = '"+village[0]+"'")
				cursor.execute("INSERT INTO dawactivity_activity(activityText, activityDate,owner_id) VALUES ('Ha finalizado la mejora de tu granja al nivel "+ str(level)+".',CURRENT_DATE,'"+village[0]+"')")
			elif upgrade[1] == 2: #wood
				level = village[5]+1
				dailyWood = round(village[2]*1.1)
				cursor.execute("UPDATE dawactivity_village SET woodLevel = "+str(level)+", dailyWood = "+str(dailyWood)+" WHERE villageName = '"+village[0]+"'")
				cursor.execute("INSERT INTO dawactivity_activity(activityText, activityDate,owner_id) VALUES ('Ha finalizado la mejora de tu aserradero al nivel "+str(level)+".',CURRENT_DATE,'"+village[0]+"')")
			elif upgrade[1] == 3: #stone
				level = village[6]+1
				dailyStone = round(village[3]*1.1)
				cursor.execute("UPDATE dawactivity_village SET stoneLevel = "+str(level)+", dailystone = "+str(dailyStone)+" WHERE villageName = '"+village[0]+"'")
				cursor.execute("INSERT INTO dawactivity_activity(activityText, activityDate,owner_id) VALUES ('Ha finalizado la mejora de tu cantera al nivel "+ str(level)+".',CURRENT_DATE,'"+village[0]+"')")
			elif upgrade[1] == 4: #wall
				level = village[7]+1
				cursor.execute("UPDATE dawactivity_village SET wallLevel = "+str(level)+" WHERE villageName = '"+village[0]+"'")
				cursor.execute("INSERT INTO dawactivity_activity(activityText, activityDate,owner_id) VALUES ('Ha finalizado la mejora de tu muralla al nivel "+ str(level)+".',CURRENT_DATE,'"+village[0]+"')")
			elif upgrade[1] == 5: #storage
				level = village[8]+1
				cursor.execute("UPDATE dawactivity_village SET storageLevel = "+str(level)+" WHERE villageName = '"+village[0]+"'")
				cursor.execute("INSERT INTO dawactivity_activity(activityText, activityDate,owner_id) VALUES ('Ha finalizado la mejora de tu almacén al nivel "+ str(level)+".',CURRENT_DATE,'"+village[0]+"')")
		cursor.execute("UPDATE dawactivity_upgrade SET completed = 1 WHERE id = "+str(upgrade[0]))
		connection.commit()
	connection.close()
	return True

def processTraining():
	connection = sqlite3.connect('/home/jcgd/Documents/Grow_your_empire/DAWActivity/db.sqlite3')
	cursor = connection.cursor()
	trainings = cursor.execute('SELECT id,village_id, units FROM dawactivity_training WHERE completed = 0').fetchall()
	 #[id,village, units]
	for training in trainings:
		#[villageName, soldiers]
		village = cursor.execute("SELECT villageName,soldiers FROM dawactivity_village WHERE villageName = '"+str(training[1])+"'").fetchone()
		if village != None:
			soldiers =village[1]+training[2]
			cursor.execute("UPDATE dawactivity_village SET soldiers = "+str(soldiers)+" WHERE villageName = '"+str(training[1])+"'")
			cursor.execute("INSERT INTO dawactivity_activity(activityText, activityDate,owner_id) VALUES ('Ha finalizado el entrenamiento de "+ str(training[2])+" unidades.',CURRENT_DATE,'"+str(village[0])+"')")
		cursor.execute("UPDATE dawactivity_training SET completed = 1 WHERE id = "+str(training[0]))
		connection.commit()
	connection.close()
	return True
	
def processAttack():
	connection = sqlite3.connect('/home/jcgd/Documents/Grow_your_empire/DAWActivity/db.sqlite3')
	cursor = connection.cursor()
	attacks = cursor.execute('SELECT id,attacker_id, defendant_id,usedSoldiers FROM dawactivity_attack WHERE completed = 0 ORDER BY registeredDateTime ASC').fetchall()
	 #[id,attacker,defendant,usedSoldiers]
	for attack in attacks:
		#[villageName, soldiers,storedWood,storedFood,storedStone]
		attacker = cursor.execute("SELECT villageName,soldiers,storedWood,storedFood,storedStone FROM dawactivity_village WHERE villageName = '"+str(attack[1])+"'").fetchone()
		#[villageName,soldiers,wallLevel,storedWood,storedFood,storedStone,storageLevel]
		defendant = cursor.execute("SELECT villageName,soldiers,wallLevel,storedWood,storedFood,storedStone, storageLevel FROM dawactivity_village WHERE villageName = '"+str(attack[2])+"'").fetchone()
		if attacker != None and defendant != None:
			defendant_virtualUnits = round(defendant[1]*(1+0.1*defendant[2]))
			print(defendant_virtualUnits)
			if attack[3] > defendant_virtualUnits: #attacker wins
				availableResources = [round(defendant[3]*(1-0.1*defendant[6])),round(defendant[4]*(1-0.1*defendant[6])),round(defendant[5]*(1-0.1*defendant[6]))]
			
				cursor.execute("UPDATE dawactivity_village SET soldiers = 0,storedWood = "+str(defendant[3]-availableResources[0])+", storedFood = "+str(defendant[4]-availableResources[1])+", storedStone = "+str(defendant[5]-availableResources[2])+" WHERE villageName = '"+str(defendant[0])+"'")
				cursor.execute("UPDATE dawactivity_village SET soldiers = "+str(attacker[1]+attack[3]-defendant_virtualUnits)+",storedWood = "+str(attacker[2]+availableResources[0])+", storedFood = "+str(attacker[3]+availableResources[1])+", storedStone = "+str(attacker[4]+availableResources[2])+" WHERE villageName = '"+str(attacker[0])+"'")
				cursor.execute("INSERT INTO dawactivity_activity(activityText, activityDate,owner_id) VALUES ('"+attacker[0]+" Te ha atacado. Has perdido "+str(defendant[1])+" soldados y te han saqueado "+str(availableResources[0])+" de madera, "+str(availableResources[2])+" de piedra y "+str(availableResources[1])+" de alimento.',CURRENT_DATE,'"+str(defendant[0])+"')")
				cursor.execute("INSERT INTO dawactivity_activity(activityText, activityDate,owner_id) VALUES ('Has atacado a "+str(attack[2])+" y has ganado. Han vuelto "+str(round(attack[3]-defendant_virtualUnits))+" soldados y has saqueado "+str(availableResources[0])+" de madera, "+str(availableResources[2])+" de piedra y "+str(availableResources[1])+" de alimento.',CURRENT_DATE,'"+str(attacker[0])+"')")
			else: #defendant wins
				cursor.execute("UPDATE dawactivity_village SET soldiers = "+str(round(defendant[1]-attack[3]*(1-0.1*defendant[2])))+" WHERE villageName = '"+str(defendant[0])+"'")
				cursor.execute("INSERT INTO dawactivity_activity(activityText, activityDate,owner_id) VALUES ('"+attack[1]+" Te ha atacado. Has perdido "+str(round(attack[3]*(1-0.1*defendant[2])))+" soldados, pero no has perdido recursos',CURRENT_DATE,'"+str(defendant[0])+"')")
				cursor.execute("INSERT INTO dawactivity_activity(activityText, activityDate,owner_id) VALUES ('Has atacado a "+str(attack[2])+" y has perdido.',CURRENT_DATE,'"+str(attacker[0])+"')")
		cursor.execute("UPDATE dawactivity_attack SET completed = 1 WHERE id = "+str(attack[0]))
		connection.commit()
	connection.close()
	return True
	
def addResources():
	connection = sqlite3.connect('/home/jcgd/Documents/Grow_your_empire/DAWActivity/db.sqlite3')
	cursor = connection.cursor()
	villages = cursor.execute('SELECT villageName,storedWood,storedFood,storedStone,dailyWood,dailyFood,dailyStone,owner_id FROM dawactivity_village WHERE disabled != true').fetchall()
	#[villageName,storedWood,storedFood,storedStone,dailyWood,dailyFood,dailyStone,owner]
	for village in villages:
		bonuses = cursor.execute("SELECT id,village_id,bonusAmount FROM dawactivity_bonus WHERE village_id = '"+str(village[0])+"' AND completed = 0 AND bonusType = 0")
		#[id,village,amount]
		bonus = bonuses.fetchone()
		totalMultiplier = 1.0
		while bonus != None:
			totalMultiplier+=(bonus[2]/10)
			cursor.execute("UPDATE dawactivity_bonus SET completed = 1 WHERE id = "+str(bonus[0]))	
			bonus = bonuses.fetchone()
		
		cursor.execute("UPDATE dawactivity_village SET storedWood = "+str(village[1]+(village[4]*totalMultiplier))+", storedFood = "+str(village[2]+(village[5]*totalMultiplier))+", storedStone = "+str(village[3]+(village[6]*totalMultiplier))+" WHERE villageName = '"+village[0]+"'")
		connection.commit()
	connection.close()
	return True

def processBonuses():
	connection = sqlite3.connect('/home/jcgd/Documents/Grow_your_empire/DAWActivity/db.sqlite3')
	cursor = connection.cursor()
	bonuses = cursor.execute("SELECT id,village_id,bonusAmount,bonusType FROM dawactivity_bonus WHERE completed = 0 AND bonusType != 0").fetchall()
	 #[id,village,amount,bonusType]
	for bonus in bonuses:
		village = cursor.execute("SELECT villageName,soldiers,woodLevel,foodLevel,stoneLevel,wallLevel,storageLevel,dailyWood,dailyFood,dailyStone FROM dawactivity_village WHERE villageName = '"+bonus[1]+"'").fetchone()
		if bonus[3] == 1 and village != None: #units
			#[villageName,soldiers,woodLevel,foodLevel,stoneLevel,wallLevel,storageLevel,dailyWood,dailyFood,dailyStone]
				cursor.execute("UPDATE dawactivity_village SET soldiers = "+str(village[1]+bonus[2])+" WHERE villageName = '"+village[0]+"'")
		elif bonus[3] == 2 and village != None: #building
			if bonus[2] == 0: #wood
				cursor.execute("UPDATE dawactivity_village SET woodLevel = "+str(village[2]+1)+", dailyWood = "+str(round(village[7]*1.1))+" WHERE villageName = '"+village[0]+"'")
			elif bonus[2] == 1: #food
				cursor.execute("UPDATE dawactivity_village SET foodLevel = "+str(village[3]+1)+", dailyFood = "+str(round(village[8]*1.1))+" WHERE villageName = '"+village[0]+"'")
			elif bonus[2] == 2: #stone
				cursor.execute("UPDATE dawactivity_village SET stoneLevel = "+str(village[4]+1)+", dailyStone = "+str(round(village[9]*1.1))+" WHERE villageName = '"+village[0]+"'")					
			elif bonus[2] == 3: #walls
				cursor.execute("UPDATE dawactivity_village SET wallLevel = "+str(village[5]+1)+" WHERE villageName = '"+village[0]+"'")
			elif bonus[2] == 4: #storage
				cursor.execute("UPDATE dawactivity_village SET storageLevel = "+str(village[6]+1)+" WHERE villageName = '"+village[0]+"'")
		cursor.execute("UPDATE dawactivity_bonus SET completed = 1 WHERE id = "+str(bonus[0]))
		connection.commit()
	connection.close()
	return True

def disableVillages():
	connection = sqlite3.connect('/home/jcgd/Documents/Grow_your_empire/DAWActivity/db.sqlite3')
	cursor = connection.cursor()
	cursor.execute("UPDATE dawactivity_village SET disabled = 1 where lastLogin < (SELECT DATETIME ('now','-14 day'))")
	connection.commit()
	connection.close()
	return True

def main():
	disableVillages()
	print("inactive villages disabled")
	processBonuses()
	print("bonuses processed")
	processUpgrades()
	print("upgrades processed")
	processTraining()
	print("trainings processed")
	processAttack()
	print("attacks processed")
	addResources()
	print("resources added")

if __name__ == "__main__":
    main()
