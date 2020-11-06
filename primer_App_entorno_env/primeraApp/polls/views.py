from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
#from django.template import loader


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'

# Create your views here.
"""
def index(resquest):
    question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('index.html')
    context = {
        'question_list': question_list
    }
    return render(resquest, 'index.html', context)
    #return HttpResponse(template.render(context, resquest))
    #output = ', '.join([q.question_text for q in question_list])
    #return HttpResponse(output)
    #return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    '''try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("ESTA PREGUNTA NO ESTA EN BASE DE DATOS") # restpuesta erro '''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question,})
"""

def vote(request, question_id):

    #print(str(request.POST['choice']))
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return HttpResponse("Error en el choice" )

    else:
        selected_choice.votes += 1
        selected_choice.save() # guarda en base de datos
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))