

from django.shortcuts import render

from DAWActivity.models import Test,Question,Option,TestResolution,Bonus,Village

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
			if question.questionType == 0:
				solutions.append(Option.objects.get(questionText=question.questionText,correctOption=True).questionOptionText)
			elif question.questionType == 1:
				solutions.append(question.expectedText)
			if solutions[len(solutions)-1] == choices[len(choices)-1]:
				points +=1
			else:
				errors.append(len(choices))
				

		if not(TestResolution.objects.filter(testName=testN,userName=request.user).exists()):
			t = TestResolution(testName=Test(testName=testN),userName=request.user,points=points)
			b = Bonus(village=Village.objects.get(owner = request.user),bonusType=0,bonusAmount=int(points*10/len(solutions)),completed=0)
			b.save()
			t.save()
			alreadyDone = ''
		else:
			alreadyDone = "Ya has realizado este test. No se han obtenido bonus adicionales"
		if (points == len(solutions)):
			text = "No has tenido ningún fallo, ¡Enhorabuena!"
		else:
			text = "Fallo en las preguntas "+str(errors)[1:-1]
		return render(request,'DAWActivity/results.html',{'points':points,'totalPoints':len(solutions),'choices':choices,'solutions':solutions,'text':text,'done':alreadyDone})