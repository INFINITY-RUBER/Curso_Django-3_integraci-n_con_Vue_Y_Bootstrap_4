## instalacion
* entorno virtual venv
`sudo apt install -y python3-venv`
otras formas 
`pip3 install virtualenv`  o 
`pip install virtualenv` 



* crear el entorno virtual:
`python3 -m venv my_carpeta_proyec`
otra forma
`virtualenv primer_App`

activar:
`source bin/activate`
`deactivate`

* Install Django:
https://docs.djangoproject.com/es/3.1/intro/tutorial01/

`pip install Django`

valida la instalacion
`python -m django --version` 

## 1 Creando un proyecto:

`django-admin startproject my_proyect`

cd /carpeta de archivo manage.py /

* Run Server
`python manage.py runserver`


## 2 Creando una Aplicacion:
Para crear su aplicación, asegúrese de que está en el mismo directorio que el archivo manage.py y escriba este comando:
`python manage.py startapp polls`


### Escriba su primera vista¶
Vamos a escribir la primera vista. Abra el archivo `polls/views.py` y ponga el siguiente código Python en ella: polls/views.
```
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

Para crear una URLconf en el directorio encuestas, cree un archivo llamado `urls.py`. El directorio de su aplicación debe verse así:
```
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
] 
```
El siguiente paso es señalar la URLconf raíz en el módulo polls.urls. En `mysite/urls.py` añada un import para django.urls.include e inserte una include() en la lista urlpatterns , para obtener:
``` 
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```
## Tutorial 2 Configuración de la base de datos
https://docs.djangoproject.com/es/3.1/intro/tutorial02/
Ahora, abra el archivo mysite/settings.py. Es un módulo normal de Python con variables de nivel de módulo que representan la configuración de Django.

Por defecto la configuración utiliza SQLite. Si tiene poca experiencia con bases de datos o su interés es solo probar Django esta es la opción más fácil. SQLite está incluido en Python por lo que no tendrá que instalar nada más para soportar su base de datos. Sin embargo, al iniciar su primer proyecto real, es posible que desee utilizar una base de datos más potente como PostgreSQL para evitar dolores de cabeza en el futuro al tener que cambiar entre base de datos.

Si desea utilizar otra base de datos, instale los conectores de base de datos apropiados, y cambie las siguientes claves en el ítem DATABASES 'default' para que se ajusten a la configuración de conexión de la base de datos:

ENGINE – bien sea 'django.db.backends.sqlite3', 'django.db.backends.postgresql_psycopg2', 'django.db.backends.mysql', o 'django.db.backends.oracle'. Otros backends también están disponibles.

Si no está utilizando SQLite como su base de datos, se deben añadir ajustes adicionales tales como **USER**, **PASSWORD**, y **HOST** se deben añadir. Para más información, vea la documentación de referencia para **DATABASES**.

Algunas de estas aplicaciones utilizan al menos una tabla de base de datos, por lo que necesitamos crear las tablas en la base de datos antes de poder utilizarlas. Para ello, ejecute el siguiente comando:

**`python manage.py migrate`**  # crea todas las tablas necesaria en la base de dato

Estos conceptos están representados por clases de Python. Edite el archivo `polls / models.py` para que tenga este aspecto:
```
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```
Para incluir la aplicación en nuestro proyecto necesitamos agregar una referencia a su clase de configuración en la configuración INSTALLED_APPS. La clase PollsConfig está en el archivo **polls/apps.py** por lo que su ruta punteada es 'polls.apps.PollsConfig'. Edite el archivo `mysite/settings.py` y agregue la ruta punteada a la configuración INSTALLED_APPS. Se verá así:
mysite/settings.py¶
```
INSTALLED_APPS = [
    *'polls.apps.PollsConfig'*, ### lo que se agrega ###
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] 
```
Ahora Django sabe incluir la aplicación polls. Vamos a ejecutar otro comando:

`python manage.py makemigrations polls`

Hay un comando que ejecutará las migraciones para usted y gestionará el esquema de base de datos automáticamente; este se denomina migrate, y hablaremos de ello en un momento, pero primero, vamos a ver cuál SQL esa migración ejecutaría . El comando sqlmigrate recibe nombres de migración y devuelve su SQL:

`python manage.py sqlmigrate polls 0001`

A continuación, ejecute de nuevo el comando migrate para crear esas tablas modelos en su base de datos:

` python manage.py migrate`

### Jugando con la API
Ahora vayamos al shell interactivo de Python y juguemos con la API gratuita que Django le proporciona. Para llamar el shell de Python, utilice este comando:

`python manage.py shell`

se nos abre otra terminal y ejecutamos:

`from polls.models import Choice, Question` # Importe las clases modelo que acabamos de escribir.

`Question.objects.all()`  #Aún no hay preguntas en el sistema

>>> from django.utils import timezone # libreria para traer la hora
>>> `timezone.now()`

>>> `q = Question(question_text="What's new?", pub_date=timezone.now())`

# Guarde el objeto en la base de datos. Tienes que llamar a save () explícitamente.
>>> `q.save()`

`Question.objects.all()`  #ver lo que creamos

# Now it has an ID.
>>> `q.id`
1

# Access model field values via Python attributes.
>>> `q.question_text`
"What's new?"
>>> `q.pub_date`
datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=<UTC>)

# Change values by changing the attributes, then calling save().
>>> `q.question_text = "What's up?"`
>>> `q.save()`

# objects.all() displays all the questions in the database.
>>> `Question.objects.all()`
<QuerySet [<Question: Question object (1)>]>

## creamos un Choice 
`c = q.choice_set.create(choice_text='Just hacking again', votes=0)`
`c.question`
`c.choice_text`
`Choice.objects.all()`

`q.choice = c`
`q.choice.question = q`

`q.choice.question.save()`

## personalizar la salida :
en el archivo **polls/models.py** y agregando un metodo __str__() a los dos modelos, Question y Choice:
```polls/models.py¶
from django.db import models

class Question(models.Model):
    # ...
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    # ...
    def __str__(self):
        return self.choice_text

```

# Presentando el sitio administrativo de Django

### Creando un usuario del admin
Primero tendremos que crear un usuario que pueda iniciar sesión en el sitio administrativo. Ejecute el siguiente comando:
`python manage.py createsuperuser`

**Username: admin**
A continuación se le solicitará su dirección de correo electrónico deseada:

**Email address: admin@example.com**

Password: **********
Password (again): *********
Superuser created successfully.

### Inicie el servidor de desarrollo¶
El sitio administrativo de Django se activa de forma predeterminada. Vamos a iniciar el servidor de desarrollo y a explorarlo. Si el servidor no está en marcha, inícielo de la siguiente forma:
`python manage.py runserver`

# Escribiendo más vistas
A continuación vamos a agregar más vistas a **polls/views.py**. Estas vistas son un poco diferentes porque toman un argumento:
```polls/views.py¶
def index(resquest):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    return HttpResponse("Esta en: detail >>  Hola Bienvendo a Django Ruber: %s." % question_id)

def Results(request, question_id):
    response = "Esta en: Results >>  Hola Bienvendo a Django Ruber: %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("Esta en: vote >>  Hola Bienvendo a Django Ruber: %s." % question_id)
```

Una estas nuevas vistas al módulo **polls.urls** añadiendo las siguientes llamadas **path()**:
```polls/urls.py¶
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

```
# Escriba vistas que realmente hagan algo¶
Cada vista es responsable de hacer una de dos cosas: retornar un objeto HttpResponse con el contenido de la página solicitada, o levantar una excepción como Http404. El resto depende de usted.
```polls/views.py¶
from django.http import HttpResponse

**from .models import Question**


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
```
# Temples
Dentro del directorio de plantillas que acaba de crear, cree otro directorio llamado sondeos y dentro de él cree un archivo llamado `index.html`. En otras palabras, su plantilla debe estar en **polls / templates / polls / `index.html`**. Debido a cómo funciona el cargador de plantillas de app_directories como se describe anteriormente, puede hacer referencia a esta plantilla dentro de Django como **polls / `index.html`**.
```polls/templates/polls/index.html¶
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

Ahora vamos a actualizar nuestra vista index en **polls/views.py** para usar la plantilla:
```polls/views.py¶
from django.http import HttpResponse
**from django.template import loader**

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


```
# Un atajo: render()¶
Es una práctica muy común cargar una plantilla, llenar un contexto y retornar un objeto `HttpResponse` con el resultado de la plantilla creada. Django proporciona un atajo. A continuación la vista `index()` completa, reescrita:
```polls/views.py
from django.shortcuts import render
from .models import Question

def index(request):
    question_list = Question.objects.order_by('-pub_date')[:5]
    
    context = {
        'question_list': question_list
    }
    return render(resquest, 'index.html', context)
```
# Levantar un error 404¶
Ahora vamos a abordar la vista de detalle de la pregunta: la página que muestra el texto de pregunta para una encuesta determinada. Aquí está la vista:
```polls/views.py¶
**from django.http import Http404**
from django.shortcuts import render

from .models import Question
# ...
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

```
# Un atajo get_object_or_404()¶
Es una práctica muy común utilizar `get()` y levantar la excepción **Http404** si no existe el objeto. Django proporciona un atajo. Aquí está la vista `detail()`, escrita:
```polls/views.py¶
from django.shortcuts import **get_object_or_404**, render

from .models import Question
# ...
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
```
# Utilice el sistema de plantillas¶
Vuelva a la vista detail() para nuestra aplicación encuesta. Teniendo en cuenta la variable de contexto question, así es como la plantilla **polls/detail.html** podría verse:
```templates/polls/detail.html¶
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```
# Quitar URLs codificadas de manera predeterminada en las plantillas¶
Recuerde que cuando escribimos el enlace para una pregunta en la plantilla **polls/index.html**, el enlace estaba parcialmente codificado de forma predeterminada como este:
`<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>`
El problema con este método de codificación predeterminada y estrechamente acoplada es que se hace difícil modificar las URLs en proyectos que tengan muchas plantillas. Sin embargo, puesto que usted definió el argumento de nombre en las funciones path() en el módulo polls.urls, usted puede eliminar la dependencia en rutas URL específicas definida en su configuración de URL usando la etiqueta de plantilla {% url %}:

`<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>`

# Asignando los nombres de URLs¶
El proyecto tutorial solo tiene una aplicación; polls. En proyectos reales de Django, puede haber cinco, diez, veinte o más aplicaciones. ¿Cómo diferencia Django los nombres de las URLs entre ellos? Por ejemplo, la aplicación polls tiene una vista detail, como la podría tener también una aplicación en el mismo proyecto que es para un blog. ¿Cómo hacer para que Django sepa cual vista de aplicaciones crear para una URL cuando se utiliza la etiqueta de plantilla`` {% url%}``?

La solución es añadir espacios de nombres a su URLconf. En el archivo **polls/urls.py**, añada un app_name para configurar el espacio de nombres de la aplicación:
```polls/urls.py¶
from django.urls import path

from . import views

**app_name = 'polls'**
urlpatterns = [
    path('', views.index, name='index'),
    ......
]

**para señalar la vista de detalle con espacio de nombres:**

polls/index.html¶
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>

```
# Write a minimal form¶
Vamos a actualizar nuestra plantilla de detalles de encuestas («polls/detail.html») a partir del último tutorial, de modo que la plantilla contenga un elemento HTML <form>:
```polls/detail.html¶
<h1>{{ question.question_text }}</h1>

{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
{% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
{% endfor %}
<input type="submit" value="Vote">
</form>
```
También creamos una implementación simulada de la función vote(). Vamos a crear una versión real. Agregue lo siguiente a polls/views.py:
```polls/views.py¶
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question
# ...
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```
Después de que alguien vota en una pregunta, la vista `vote()` remite a la página de resultados de la pregunta. Vamos a escribir dicha vista:
Esto es casi exactamente lo mismo que la vista detail() del Tutorial 3. La única diferencia es el nombre de la plantilla. Solucionaremos esta redundancia más tarde.
Ahora, cree una template polls/results.html:
```polls/views.py¶
from django.shortcuts import get_object_or_404, render


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
```templates/polls/results.html¶
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
{% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```
# Modifique las vistas¶
A continuación, vamos a eliminar nuestras viejas vistas index, detail y results y en su lugar vamos a usar las vistas genéricas de Django. Para ello, abra el archivo polls/views.py y modifíquelo de la siguiente manera:

Primero, abra el URLconf **polls/urls.p**y y modifíquelo de la siguiente manera:
```polls/urls.py¶
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```
```polls/views.py¶
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    ... # same as above, no changes needed.
```
# CSS Personalice la apariencia de su aplicación

Introduzca el siguiente código en esa hoja de estilo (**polls/static/style.css**):
```/style.css¶
li a {
    color: green;
}
```
A continuación, agregue lo siguiente en la parte superior de /**templates/polls/index.html**:

```polls/templates/index.html¶

{% load static %}

<link rel="stylesheet"  href="{% static 'css/style.css' %}">
```
# Personalice el formulario del sitio administrativo P-7
Al registrar el modelo Question con admin.site.register (**Question**)`, Django pudo construir una representación del formulario predeterminado. A menudo, usted querrá personalizar el aspecto y el funcionamiento del formulario del sitio administrativo. Usted hará esto indicándole a Django las opciones que desee cuando registre el objeto.
Veamos cómo funciona esto reordenando los campos en el formulario de edición. Reemplace la línea **admin.site.register(Question)**con:
```polls/admin.py¶

from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']

admin.site.register(Question, QuestionAdmin)

```
# Agregando objetos relacionados
OK, tenemos nuestra página de administración Question, pero una Question tiene varias `Choices`, y la página de administración no muestra opciones.
```polls/admin.py¶

from django.contrib import admin
from .models import **Choice**, Question

class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']


admin.site.register(Question, QuestionAdmin)
`admin.site.register(Choice)`
```
# fieldsets por el fields y ChoiceInline
Esto le indica a Django: «Los objetos Choice se editan en la página de administración Question. De forma predeterminada, proporciona suficientes campos para 3 opciones.»
```polls/admin.py¶

from django.contrib import admin
from .models import Choice, Question


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    **`fieldsets`** = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
```
Por defecto, Django muestra el str() de cada objeto, pero a veces sería más útil si pudiéramos mostrar los campos individuales. Para hacerlo, utilice la opción del sitio administrativo :attr::~django.contrib.admin.ModelAdmin.list_display, que es una tupla de nombres de campos para que se muestre como columnas en la página de lista de cambios para el objeto:
```/admin.py¶

class QuestionAdmin(admin.ModelAdmin):
    # ...
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    
```
Edite de nuevo su archivo polls/admin.py y añada una mejora a la página Question en la lista de cambios: filtre utilizando el **list_filter**. Agregue la siguiente línea a QuestionAdmin:

`list_filter = ['pub_date']`

Esto se perfila bien. Vamos a añadir un poco de capacidad de búsqueda:

`search_fields = ['question_text']`

# Personalice el aspecto del sitio administrativo
Cree un directorio templates en el directorio de su proyecto (el que contiene manage.py). Las plantillas se pueden ubicar en cualquier parte de su sistema de archivos al que Django pueda acceder. (Django ejecuta como cualquier usuario ejecuta su servidor.) Sin embargo, una buena práctica a seguir es guardar sus plantillas en el proyecto.

Abra el archivo de configuraciones (mysite/settings.py, recuerde) y añada una opción DIRS en la opción TEMPLATES

```mysite/settings.py¶
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
       ** 'DIRS': [BASE_DIR / 'templates'],**
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
] 
```
DIRS es una lista de directorios del sistema de archivos utilizada para comprobar cuando se cargan las plantillas de Django; es una ruta de búsqueda.
Ahora cree un directorio llamado `admin` dentro de templates y copie la plantilla **admin/base_site.html** desde dentro del directorio de plantillas predeterminado del sitio administrativo de Django en el código fuente de Django (**django/contrib/admin/templates**) en ese directorio.
¿Dónde están los archivos fuente de Django?

Si tiene dificultad para encontrar donde están localizados los archivos fuente de Django en su sistema, ejecute el siguiente comando:
`python -c "import django; print(django.__path__)"`
**'/home/ruber/.local/lib/python3.8/site-packages/django'**
```
{% extends "admin/base.html" %}

{% block title %}{{ title }} | {{ site_title|default:_('Django site admin') }}{% endblock %}

{% block branding %}
<h1 id="site-name"><a href="{% url 'admin:index' %}">Hola Ruber Hernandez {{ site_header|default:_('Django administration') }}</a></h1>
{% endblock %}

{% block nav-global %}{% endblock %}
```

