from django.db import models
from django.contrib.auth.models import User as User

# Create your models here.

class Student(models.Model):
	user = models.OneToOneField(User,on_delete = models.CASCADE)
	subject = models.IntegerField("Subject")
	def __str__(self):
		return str(self.user)+'-'+str(self.subject)

class Test (models.Model):
	testName = models.TextField("Test name", primary_key=True)
	date = models.DateTimeField("Available from")
	subject = models.IntegerField("Subject") #0 = prog, 1 = BBDD, 2 = EH
	def __str__(self):
		return self.testName+'-'+str(self.subject)

QUESTION_OPTIONS = (
	('a','a'),
	('b', 'b'),
	('c','c'),
	('d','d'),
)

class Question(models.Model):
	questionText =  models.TextField("Question", primary_key=True)
	questionOption1 = models.TextField("Option 1")
	questionOption2 = models.TextField("Option 2")
	questionOption3 = models.TextField("Option 3")
	questionOption4 = models.TextField("Option 4")
	correctOption = models.CharField("Correct option",max_length=1,choices=QUESTION_OPTIONS,default="a")
	testName = models.ForeignKey(
		Test,
		on_delete = models.CASCADE,
	)

	def __str__(self):
		return self.questionText


class TestResolution(models.Model):
	testName = models.ForeignKey(
		Test,
		on_delete = models.CASCADE,
	)
	userName = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)
	points = models.IntegerField("Points obtained")

	def __str__(self):
		return self.testName.testName+'-'+self.userName.username

class Village(models.Model):
	villageName = models.TextField("Village Name", primary_key=True)
	dailyFood = models.IntegerField("Daily food obtained")
	dailyWood = models.IntegerField("Daily wood obtained")
	dailyStone = models.IntegerField("Daily stone obtained")
	storedFood = models.IntegerField("Total food stored")
	storedWood = models.IntegerField("Total wood stored")
	storedStone = models.IntegerField("Total stone stored")
	foodLevel = models.IntegerField("Food level")
	woodLevel = models.IntegerField("Wood level")
	stoneLevel = models.IntegerField("Stone level")
	wallLevel = models.IntegerField("Walls level")
	storageLevel = models.IntegerField("Storage level")
	soldiers = models.IntegerField("Amount of units")
	lastLogin = models.DateField("Last login")
	disabled = models.BooleanField("Disabled")
	owner = models.ForeignKey(
		User,
		on_delete = models.CASCADE,
	)

	def __str__(self):
		return self.villageName

class Activity (models.Model):
	activityText = models.TextField("Activity description")
	activityDate = models.DateField("Time registered")
	owner = models.ForeignKey(
                Village,
                on_delete = models.CASCADE, 
        )

	def __str__(self):
		return self.activityText+'-'+str(self.activityDate)+'-'+self.owner.villageName

class Attack(models.Model):
	attacker = models.ForeignKey(
                Village,
                on_delete = models.CASCADE,
		related_name="Attacker" 
        )
	defendant = models.ForeignKey(
                Village,
                on_delete = models.CASCADE,
		related_name="Defendant" 
        )
	usedSoldiers = models.IntegerField("Soldiers")
	registeredDateTime = models.DateTimeField("Registration date")
	completed = models.BooleanField("Completed")
	def __str__(self):
		return self.attacker.villageName+'-'+self.defendant.villageName+'-'+str(self.registeredDateTime)

class TradeOffer(models.Model):
	source = models.ForeignKey(
                Village,
                on_delete = models.CASCADE,
		related_name="Source" 
        )
	destination = models.ForeignKey(
                Village,
                on_delete = models.CASCADE,
		related_name="Destination" 
        )
	wantedWood = models.IntegerField("Wanted wood")
	wantedFood = models.IntegerField("Wanted food")
	wantedStone = models.IntegerField("Wanted stone")
	offeredWood = models.IntegerField("Offered wood")
	offeredFood = models.IntegerField("Offered food")
	offeredStone = models.IntegerField("Offered stone")
	accepted = models.BooleanField("Offering accepted")

	def __str__(self):
		return self.source.villageName+'-'+self.destination.villageName

class Upgrade(models.Model):
	village = models.ForeignKey(
	Village,
	on_delete=models.CASCADE,
	)
	level=models.IntegerField("Level to upgrade to")
	building=models.IntegerField("Building")
	woodCost=models.IntegerField("WoodCost")
	stoneCost=models.IntegerField("StoneCost")
	completed=models.BooleanField("Completed")

	def __str__(self):
		return self.village.villageName+'-'+str(self.building)

class Training(models.Model):
	village = models.ForeignKey(
	Village,
	on_delete=models.CASCADE,
	)
	units=models.IntegerField("Units")
	foodCost=models.IntegerField("FoodCost")
	completed=models.BooleanField("Completed")

	def __str__(self):
		return self.village.villageName+'-'+str(self.units)

class Bonus(models.Model):
	village = models.ForeignKey(
	Village,
	on_delete = models.CASCADE,
	)
	bonusType = models.IntegerField("Bonus type") # 0 = resources, 1 = units, 2 = building
	bonusAmount = models.IntegerField("Bonus amount")
	completed = models.BooleanField("Completed")

class New(models.Model):
	title = models.TextField("Title")
	desc = models.TextField("Description")
	newDate = models.DateField("New date")
	def __str__(self):
		return self.title
