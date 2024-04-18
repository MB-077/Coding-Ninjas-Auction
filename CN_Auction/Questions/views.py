from django.shortcuts import render
from django.http import JsonResponse
from .models import Question

# Create your views here.
def send_questions():
    questions = Question.objects.all()
    data = []
    data_format = {}
    for x in questions:
        data_format= {
            'question' : x.question_text,
            'options' : [x.option_1, x.option_2, x.option_3, x.option_4],
            'correctAnswer' : x.correct_option
        }
        data.append(data_format)

    return JsonResponse({"data" : data, "n" : len(data)})