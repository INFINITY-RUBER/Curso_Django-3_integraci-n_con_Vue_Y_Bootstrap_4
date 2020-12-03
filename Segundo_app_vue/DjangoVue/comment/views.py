from django.http import response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.template import loader
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils.translation import gettext as _

from .models import Comment, Contact
from .forms import CommentForm, ContactForm

import logging
import csv


# Get an instance of a logger
logger = logging.getLogger(__name__)

def export(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="DatosTest.csv"'
    
    comments = Comment.objects.all()
    writer = csv.writer(response)

    writer.writerow(['ID', 'COMENTARIOS'])
    for c in comments:
        writer.writerow([c.id, c.text])      
    # writer.writerow(['primera fila', 'Django','Flask','Python'])
    # writer.writerow(['primera fila', 'A','B','C', 'cUY','MAS DATOS','OTROS'])
    return response


def testview(request):    
    return render(request, 'test/testview.html')


def index(request):
    print(_("Welcome to my App") )
    logger.debug('....debug!')
    logger.info('.........info!')
    logger.error('...........error!')

    if 'comment_id' in request.session:
        print("ultimo comentario :" + str(request.session['comment_id']))
        del request.session['comment_id']

    comments = Comment.objects.all()
    paginator = Paginator(comments,3)

    page_number = request.GET.get('page')
    comments_page = paginator.get_page(page_number)

    return render(request, 'index_page.html', {'comments_page':comments_page})
    # return render(request, 'index.html', {'comments':comments})



def add(request):
    if request.method == 'POST':
        form = CommentForm(request.POST) 
        if form.is_valid():
            comment = form.save()

            html_message = loader.render_to_string('email/comment.html',{'comment':comment})

            request.session['comment_id'] = comment.id

            send_mail(
                "Comentario #" +str(comment.id), # "Titulo",
                comment.text,# "Contenido",
                "ruberhenandez@gmail.com",
                ["ruber.hernandez.333@gmail.com"],
                fail_silently=False,
                html_message = html_message
                # html_message="<h1>Hola mundo de Ruber</h1>"
            )
            return redirect('comment:index')
    else:
        form = CommentForm()  

    return render(request, 'add.html',{'form':form})
    

def update(request, pk):

    comment = get_object_or_404(Comment, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment) 

        print(form.errors.as_json())

        if form.is_valid():
            form.save(commit=True, text='Hola mundo')
            return redirect('comment:update',pk=comment.id)
    else:
        form = CommentForm(instance=comment)  

    return render(request, 'update.html',{'form': form, 'comment': comment})


from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError



@csrf_exempt
def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)

        if form.is_valid():

            if 'document'in request.FILES:
                print('FILES contenido')
            else:
                print('FILES NO contenido')

            contact = Contact()
            contact.name = form.cleaned_data['name']
            contact.surname = form.cleaned_data['surname']
            contact.phone = form.cleaned_data['phone']
            contact.email = form.cleaned_data['email']
            contact.date_birth = form.cleaned_data['date_birth']
            contact.sex = form.cleaned_data['sex']
            contact.type_contact = form.cleaned_data['type_contact']
            if 'document'in request.FILES:
                contact.document = request.FILES['document']
            contact.save()

            messages.add_message(request, messages.INFO,  'Contacto Guardado')            
            return redirect('comment:contact')
            # print('Valido: ' + form.cleaned_data['type_contact'].name)

        else:
            print('No es valido')


    else:
        form = ContactForm()
    
    print(request.FILES)
    # if (form.errors):
        # raise ValidationError(form.errors)

    return render(request, 'contact.html',{'form': form})
