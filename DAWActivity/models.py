from django.db import models
from django.contrib.auth.models import User as User
from django.utils import timezone
# Create your models here.

class Subject (models.Model):
	subjectName = models.CharField("Subject name",max_length=100, primary_key=True)
	def __str__(self):
		return self.subjectName

class Student(models.Model):
	user = models.OneToOneField(User,to_field="username",on_delete=models.CASCADE,primary_key=True)
	subject = models.ManyToManyField(Subject)
	def __str__(self):
		return str(self.user.username)

	def createVillage(self):
		Village.objects.create(
            villageName = 'Aldea de '+self.user.username,
			dailyFood = 5,
			dailyWood = 5,
			dailyStone = 3,
			storedFood = 5,
			storedWood = 5,
			storedStone = 3,
			foodLevel = 1,
			woodLevel = 1,
			stoneLevel = 1,
			wallLevel = 1,
			storageLevel = 1,
			soldiers = 5,
			lastLogin = timezone.now(),
			disabled = True,
			owner = self).save()
		return

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
		if len(Village.objects.filter(owner = self)) == 0:
			self.createVillage()

class Village(models.Model):
	villageName = models.CharField("Village Name",max_length=50)
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
	owner = models.OneToOneField(Student,to_field="user_id",on_delete=models.CASCADE,primary_key=True)

	def __str__(self):
		return self.villageName+' - '+self.owner.user_id

class Test (models.Model):
	testName = models.CharField("Test name",max_length=50)
	date = models.DateTimeField("Available from")
	subject = models.ForeignKey(
		Subject,
		to_field="subjectName",
		on_delete = models.CASCADE,
	)

	def __str__(self):
		return self.testName+'-'+str(self.subject)
	
	class Meta:
		constraints = [
            models.UniqueConstraint(
                fields=['testName'], name='Test_testName'
            )
        ]
		
QUESTION_CHOICES = [
    ("Opciones","Opciones"),
    ("Relleno","Relleno"),
]

class Question(models.Model):
	questionText =  models.CharField("Question",max_length=50)
	expectedText = models.CharField("Expected text",max_length=100,blank=True)
	questionType = models.CharField("Type",max_length=50,choices=QUESTION_CHOICES)
	testName = models.ForeignKey(
		Test,
		to_field="testName",
		on_delete = models.CASCADE,
	)

	def __str__(self):
		return self.questionText
	
	class Meta:
		constraints = [
            models.UniqueConstraint(
                fields=['questionText','testName'], name='Question_questionText_testName'
            )
        ]
	
class Option(models.Model):
	questionOptionText = models.CharField("Option 1",max_length=50)
	questionText = models.ForeignKey(
		Question,
		on_delete = models.CASCADE,
	)
	correctOption = models.BooleanField("Correct")

	def __str__(self):
		return self.questionText.questionText + ' - ' + self.questionOptionText
	
	class Meta:
		constraints = [
            models.UniqueConstraint(
                fields=['questionOptionText','questionText'], name='Option_questionText_questionOptionText'
            )
        ]

class TestResolution(models.Model):
	testName = models.ForeignKey(
		Test,
		to_field="testName",
		on_delete = models.CASCADE,
	)
	studentName = models.ForeignKey(
		Student,
		to_field="user_id",
		on_delete=models.CASCADE,
	)
	points = models.IntegerField("Points obtained")

	def __str__(self):
		return self.testName.testName+'-'+self.studentName.user_id
	
	class Meta:
		constraints = [
            models.UniqueConstraint(
                fields=['testName','studentName'], name='TestResolution_testName_studentName'
            )
        ]

class Activity (models.Model):
	activityText = models.CharField("Activity description",max_length=150)
	activityDate = models.DateTimeField("Time registered")
	owner = models.ForeignKey(
                Village,
                on_delete = models.CASCADE,
				to_field="owner"
        )

	def __str__(self):
		return self.activityText+'-'+str(self.activityDate)+'-'+self.owner.villageName
	
	class Meta:
		constraints = [
            models.UniqueConstraint(
                fields=['activityDate', 'owner','activityText'], name='Activity_date_owner_activityText'
            )
        ]

class Attack(models.Model):
	attacker = models.ForeignKey(
        Village,
        on_delete = models.CASCADE,
		to_field="owner",
		related_name="Attacker",
        )
	defendant = models.ForeignKey(
        Village,
        on_delete = models.CASCADE,
		to_field="owner",
		related_name="Defendant",
        )
	usedSoldiers = models.IntegerField("Soldiers")
	registeredDateTime = models.DateTimeField("Registration date")
	completed = models.BooleanField("Completed")

	def __str__(self):
		return self.attacker.villageName+'-'+self.defendant.villageName+'-'+str(self.registeredDateTime)
	
	class Meta:
		constraints = [
            models.UniqueConstraint(
                fields=['attacker', 'defendant', 'registeredDateTime'], name='Attack_attacker_defendant_registeredDateTime'
            )
        ]

class TradeOffer(models.Model):
	registeredDateTime = models.DateTimeField("Registration date")
	source = models.ForeignKey(
        Village,
        on_delete = models.CASCADE,
		to_field="owner",
		related_name="Source",
        )
	destination = models.ForeignKey(
        Village,
        on_delete = models.CASCADE,
		to_field="owner",
		related_name="Destination",
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

	class Meta:
		constraints = [
            models.UniqueConstraint(
                fields=['source', 'destination', 'registeredDateTime'], name='TradeOffer_source_destination_registeredDateTime'
            )
        ]

class Upgrade(models.Model):
	village = models.ForeignKey(
		Village,
		to_field="owner",
		on_delete=models.CASCADE,
		)
	registeredDateTime = models.DateTimeField("Registration date")
	level=models.IntegerField("Level to upgrade to")
	building=models.IntegerField("Building")
	woodCost=models.IntegerField("WoodCost")
	stoneCost=models.IntegerField("StoneCost")
	completed=models.BooleanField("Completed")

	def __str__(self):
		return self.village.villageName+'-'+str(self.building)
	
	class Meta:
		constraints = [
            models.UniqueConstraint(
                fields=['village','registeredDateTime'], name='Upgrade_village_registeredDateTime'
            )
        ]

class Training(models.Model):
	village = models.ForeignKey(
		Village,
		to_field="owner",
		on_delete=models.CASCADE,
	)
	registeredDateTime = models.DateTimeField("Registration date")
	units=models.IntegerField("Units")
	foodCost=models.IntegerField("FoodCost")
	completed=models.BooleanField("Completed")

	def __str__(self):
		return self.village.villageName+'-'+str(self.units)

	class Meta:
		constraints = [
            models.UniqueConstraint(
                fields=['village','registeredDateTime'], name='Training_village_registeredDateTime'
            )
        ]

class Bonus(models.Model):
	village = models.ForeignKey(
		Village,
		to_field="owner",
		on_delete = models.CASCADE,
	)
	registeredDateTime = models.DateTimeField("Registration date")
	bonusType = models.IntegerField("Bonus type") # 0 = resources, 1 = units, 2 = building
	bonusAmount = models.IntegerField("Bonus amount")
	completed = models.BooleanField("Completed")

	def __str__(self):
		return self.village.villageName+'-'+str(self.registeredDateTime)

	class Meta:
		constraints = [
            models.UniqueConstraint(
                fields=['village','registeredDateTime'], name='Bonus_village_registeredDateTime'
            )
        ]

class New(models.Model):
	title = models.CharField("Title",max_length=100)
	desc = models.CharField("Description",max_length=2000)
	registeredDateTime = models.DateTimeField("Registration date")

	def __str__(self):
		return self.title

	class Meta:
		constraints = [
            models.UniqueConstraint(
                fields=['title','registeredDateTime'], name='New_title_registeredDateTime'
            )
        ]
