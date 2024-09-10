from django.utils import timezone
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from DAWActivity.models import Question,Option,TestResolution,Bonus,Village

def correctTest(request,testN):
	if not request.user.is_authenticated:
		return render(request,'DAWActivity/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		points = 0
		errors = []
		questions = Question.objects.filter(testName=testN)
		solutions = []
		choices = []
		for question in questions:
			choices.append(request.POST[question.questionText])
			if question.questionType == "Opciones":
				solutions.append(Option.objects.filter(questionText=question,correctOption=True).first().questionOptionText)
			elif question.questionType == "Relleno":
				solutions.append(question.expectedText)
			if solutions[len(solutions)-1] == choices[len(choices)-1]:
				points +=1
			else:
				errors.append(len(choices))
				
		try:
			TestResolution.objects.get(testName = testN,studentName_id=request.user.student)
			alreadyDone = "Ya has realizado este test. No se han obtenido bonus adicionales"
		except ObjectDoesNotExist:
			TestResolution(testName_id=testN,studentName=request.user.student,points=points).save()
			Bonus(village=Village.objects.get(owner = request.user.student),bonusType=0,bonusAmount=int(points*10/len(solutions)),completed=0,registeredDateTime = timezone.now()).save()
			alreadyDone = ''
		if (points == len(solutions)):
			text = "No has tenido ningún fallo, ¡Enhorabuena!"
		else:
			text = "Fallo en las preguntas "+str(errors)[1:-1]
		return render(request,'DAWActivity/results.html',{'points':points,'totalPoints':len(solutions),'choices':choices,'solutions':solutions,'text':text,'done':alreadyDone})