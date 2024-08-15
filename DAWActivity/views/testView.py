

from django.shortcuts import render

from DAWActivity.models import Test,Question,TestResolution,Bonus,Village

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