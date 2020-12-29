# NUEVA APP CON VUE

**1- creamos una carpeta para el entorno virtual y corremos el entorno env**

**2- creamos nuestor proyecto con :**
`django-admin startproject DjangoVue`  
**3- creamos una nueva app con el comando:**
`django-admin startapp listelement`

**4 - agregamos nuestra app al settings.py de nuestor proyecto DjangoVue**

```INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    **'listelement'**
    ]
```

**5- creamos nuestras catergorias en `models.py`**

```from django.db import models


class Category(models.Model):
    title = models.CharField( max_length=255)
    url_clean = models.CharField(max_length=255)

class Type(models.Model):
    title = models.CharField( max_length=255)
    url_clean = models.CharField(max_length=255)

class Element(models.Model):
    title = models.CharField( max_length=255)
    url_clean = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
```

**6- creamos nuestra base de dato en MYSQL**
https://likegeeks.com/es/mysql-en-linux/

- `sudo apt install mysql-server` instalar
- `mysql --version` ver version
- `sudo systemctl status mysql` status
- `sudo systemctl start mysql` iniciar
- `sudo systemctl restart mysql` REINICIAR
- `sudo systemctl stop mysql` STOP
- `sudo systemctl enable mysql` habilitarlo
- `/etc/mysql/my.cnf` Archivo de configuracion
- `cat /etc/mysql/my.cnf` ver el contenido
  Saber donde esta todos los archivos de mysql
- `dpkg -L mysql-server`
  Ver los puetos que usa:
- `sudo lsof -n | grep 'mysql.*TCP'`
  `sudo netstat -tlpn | grep mysql`
  scrip para crear claves root
  `sudo mysql_secure_installation`
  Para hacer esto, primero tiene que acceder al MySQL Shell como usuario raíz:

ingreso a mysql:
$ `sudo mysql -u root -p`

Para crear un nuevo usuario corra la siguiente comando:

- `CREATE USER 'djruber'@'%' IDENTIFIED WITH mysql_native_password BY 'Eri******2018@'; `

- `CREATE DATABASE djangovueelement;` crea base de datos

- `GRANT ALL ON djangovueelement.* TO 'djruber'@'%'; `dar permiso a DB nueva al usuario
  Ahora tiene una base de datos y una cuenta de usuario, cada una creada específicamente para Django. Necesitamos vaciar los privilegios para que la instancia actual de MySQL conozca los cambios recientes que hicimos con el siguiente comando:
- `FLUSH PRIVILEGES;`

- `CREATE TABLE [table_name] (column1_name data_type(length) [NOT NULL] [DEFAULT value] [AUTO_INCREMENT], column2_name data_type(length) [NOT NULL] [DEFAULT value] [AUTO_INCREMENT] ... ); ` ejemplo
- `CREATE TABLE Person (Id int(10) NOT NULL, name varchar(10), last_name varchar(10));`
  tail -f /var/log/mysqld.log

- `SHOW DATABASES; ` # ver las BD creados
- `USE djangovueelement; ` selecionar la base de datos
- `SELECT user FROM mysql.user;` # ver los usuarios creados
- `SHOW FULL TABLES FROM djangovueelement;` ver las tablas creadas
- `SELECT * FROM table_name;` # ver datos tabla
- `describe table_name;` # describe como esta formada la tabla
- `show tables;` ver las tablas creadas
- `INSERT INTO table_name VALUES ('Fulano','1974-04-12');` insertar datos a la tabla
- `UPDATE comment_comment SET element_id=1 WHERE id=3;` actualizar un valor
- `DELETE FROM MyGuests WHERE id=3` borrar un elemento
- (sudo su en termial)
- `mysqldump -u root -p nombre_bbdd > fichero_exportación.sql` EXPORTAR base de datos
- `mysql -u root -p nombre_bbdd < ruta_fichero_importación.sql` IMPORTAR base de datos

**MySQL DB API Y CONEXION CON DJANGO**
https://www.digitalocean.com/community/tutorials/how-to-create-a-django-app-and-connect-it-to-a-database

-`sudo apt install mysql-server` -`python3 -m venv env` entorno viertual

- `env/bin/activate` activar entorno
- `pip install django`
- `sudo apt install python3-dev ` dependencias
- `sudo apt install python3-dev libmysqlclient-dev default-libmysqlclient-dev` dependencias de mysql
- `pip install mysqlclient` cliente mysql
- `sudo mysql -u root` ingreso a myql
- `SHOW DATABASES;` ver la db creadas
- `CREATE DATABASE New_data; ` crear nueva base data
- `CREATE USER 'djangouser'@'%' IDENTIFIED WITH mysql_native_password BY 'password';`
  crea usuario 'djangouser' y password -`GRANT ALL ON New_data.* TO 'djangouser'@'%';` dar permiso al usuario en la data base 'New_data' No olvidar el punto -`FLUSH PRIVILEGES;` terminar de dar privilegios a nuevos cambios

### Configurar la conexión de la aplicación con la base de datos

Ahora que somos capaces de conectarnos con una base de datos, vamos a configurar los
parámetros para conectarnos con la base de datos que creamos en el Workbench de
MySQL. **/settings.py**

```/settings.py
...
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/etc/mysql/my.cnf',
        },
    }
}
```

### editamos la configuracion de my.cnf para la conexion

`sudo nano /etc/mysql/my.cnf`

```......
[client]
database = djangovueelement
user = djruber
password = E*********2**8@
default-character-set = utf8

```

reiniciamos el server mysql
`sudo systemctl daemon-reload`
`sudo systemctl restart mysql`

**7- realizamos la migraciones de la base de datos en django**

- `python manage.py migrate`
- `python manage.py makemigrations`
- `python manage.py migrate`

**8- Registra modelos de admin a la app** -`python manage.py createsuperuser` crea usuario admin y su clave Ericsson -`python manage.py runserver `
correr el servidor de Django y luego ingresamos en admin y configuramos
los siguientes modelos
**admin.py**

```
from django.contrib import admin
from .models import Element, Category, Type

# Register your models here.
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id','title')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title')

class ElementAdmin(admin.ModelAdmin):
    list_display = ('id','title')

admin.site.register(Type, TypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Element, ElementAdmin)
```

**9- Configura la funcion **str**r**
`models.py`

```
# Create your models here.

class Category(models.Model):
    ....

    def __str__(self): # esto es la instancia del objeto que esta referenciado la clase
        return self.title

class Type(models.Model):
    ...

    def __str__(self): # esto es la instancia del objeto que esta referenciado la clase
        return self.title

class Element(models.Model):
    .....

    def __str__(self): # esto es la instancia del objeto que esta referenciado la clase
        return self.title
```

# ******\*\*******\*\*\*\*******\*\*******\*\*\*\*******\*\*******\*\*\*\*******\*\*******

# DJANGO REST Framework API https://www.django-rest-framework.org/

# ******\*\*******\*\*\*\*******\*\*******\*\*\*\*******\*\*******\*\*\*\*******\*\*******

`pip install djangorestframework` para instalar el paquete

Luego creamos un archivo `serializer.py` en nuestra app para que sea consumida por https
**listelement/serializer.py**

```
from rest_framework import serializers
from .models import Element

class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'


```

Luego creamos un archivo `viewsets.py`

**listelement/viewsets.py**

```
from rest_framework import viewsets
from .models import Element
from .serializer import ElementSerializer

class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer

```

Luego de todo esto hay que mapear todo esto en ur archivo `urls.py` como se hizo en primer ejemplo de app y configuras las libreria creadas
**listelement/urls.py**

```
from django.urls import path
from rest_framework import routers
from .viewsets import ElementViewSet

route = routers.SimpleRouter()
route.register('element', ElementViewSet)

urlpatterns = route.urls # para que genere automaticament la url

```

LUEGO VAMOS nuestro archivo Urls.py GLOBAL para resgistrar nuestra nueva ruta que esta en la aplicacion
**DjangoVue/urls.py**

```
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
  **path('api/', include('listelement.urls')),**
]
```

### Lo mas importante como dice la documentacion agregar a la app 'rest_framework'

vamos al archivo `settings.py` y agregar 'rest_framework'

```
INSTALLED_APPS = [
    .......
    ......
    'listelement',
    'rest_framework',
]
```

Luego lebantamos el server y vamos a `http://127.0.0.1:8000/api/element/` y
vemos nuestra api funcionando

# ********\*\*********\*\*********\*\*********\*\*\*********\*\*********\*\*********\*\*********

# terminar el resto de recursos modelo categoria y type

Terminamos de agregar los modelos de nuestra api:
**listelement/serializer.py**

```
from rest_framework import serializers
from .models import Element

class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


```

**listelement/viewsets.py**

```
from rest_framework import viewsets
from .models import Element, Category, Type
from .serializer import ElementSerializer, CategorySerializer, TypeSerializer

class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

```

**listelement/urls.py**

```
from django.urls import path
from rest_framework import routers
from .viewsets import ElementViewSet, CategoryViewSet, TypeViewSet

route = routers.SimpleRouter()
route.register('element', ElementViewSet)
route.register('category', CategoryViewSet)
route.register('type', TypeViewSet)

urlpatterns = route.urls
```

# PRESENTAR LA API-REST

Install Postman in Linux https://linux4one.com/how-to-install-postman-in-linux

`wget https://dl.pstmn.io/download/latest/linux64 -O postman-linux-x64.tar.gz`
Extract the downloaded file by running the following command in /opt directory:

`sudo tar -xvzf postman-linux-x64.tar.gz -C /opt`
Finally, create a symbolic link running following command in terminal:

`sudo ln -s /opt/Postman/Postman /usr/bin/postman`
After completing the above process you have successfully installed Postman on your Linux system.
Now to create a desktop icon you can run below command:

```
cat << EOF > ~/.local/share/applications/postman2.desktop
[Desktop Entry]
Name=Postman
GenericName=API Client
X-GNOME-FullName=Postman API Client
Comment=Make and view REST API calls and responses
Keywords=api;
Exec=/opt/Postman/Postman
Terminal=false
Type=Application
Icon=/opt/Postman/app/resources/app/assets/icon.png
Categories=Development;Utilities;
EOF
```

# **NODE** y su instalacion

https://nodejs.org/en/
Cómo actualizar Node.js usando n en Linux
Lo primero de todo es comprobar nuestra versión de Node.js, para ello ejecutamos en una consola lo siguiente:

`sudo npm --version`

Una vez sabemos que versión tenemos, vamos a comenzar el proceso de actualización. Lo primero de todo será limpiar la cache que genera npm.

`sudo npm cache clean -f`

El siguiente paso es instalar n, una herramienta de administración de Node.js, que nos va a ayudar bastante.

`sudo npm install -g n`

Y ahora vamos a instalar la ultima versión estable.

`sudo n stable`

Si comprobamos la versión de node que tenemos ahora mismo instalada, después de la instalación, debe coincidir con la que aparece en este listado de versiones.

`sudo npm --version`

Si deseamos instalar alguna versión en concreto podemos hacerlo de la siguiente forma: ejeplo`sudo n 6.**.**`

Y lo ultimo de todo es instalar la última versión de npm.

`npm update npm -g`

# intall VUE CLI

sudo
`npm install -g @vue/cli`
`vue --version`

**CREACION DE UN NUEO PROYECTO EN VUE:**
`vue create ` my_name-project

# DJANGO CORS- HEADERS

Agregar un ruta a la lista blanca de peticiones permitidas a nuestro backend de Django. https://pypi.org/project/django-cors-headers/

`pip install django-cors-headers`

1- agregar en nuestras configuraciones la app instalada en **setting.py**

```
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]
2  agregar tambien en nuestro MIDDLEWARE:

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    .....
    .....
]
```

3 agretar la siguiente configuracion `CORS_ALLOWED_ORIGINS = True` al inicio de nuesto **settings.py**

```
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

**CORS_ALLOWED_ORIGINS = True **
```

Luego agreamas los sitios permitidos nuestroa direcion: `"http://localhost:8080"`
`CORS_ALLOWED_ORIGINS = [
#"https://example.com",
#"https://sub.example.com",
"http://localhost:8080",

]`

# BOOTSTRAP_VUE

https://bootstrap-vue.org/
BootstrapVue Se usa para no usar Jquery que es una tecnologia vieja
se instala con NPM:
`npm install bootstrap-vue`
Luego, registre BootstrapVue en el punto de entrada de su aplicación
en **main.js**

```
import Vue from 'vue'
**import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'**

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
```

E importe archivos **CSS** Bootstrap y **BootstrapVue**:

```
import Vue from 'vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

**import 'bootstrap/dist/css/bootstrap.css'**
**import 'bootstrap-vue/dist/bootstrap-vue.css'**

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
```

# Vue Router

es completamente compatible con vue y se istala con el comando de npm:
`npm install vue-router`
Ahora agregamos estos importaciones a nuestra app en el archivo **main.js**

```
import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)
```

aquie hay unos ejemplos de configuracion:https://router.vuejs.org/guide/#html
`<router-view></router-view>` en nuestro **App.vue**

```
<template>
  <div id="app">

    <Header/>
  ** <router-view></router-view> **


  </div>

</template>
```

y en nuestro **main.js** definimos una costante para las rutas

```
const routes = [
  { path: '/', component: List }
  { path: '/Detail', component: Detail }
]
```

y tambien quitamos de nuestra **App.vue** el importe de componentes y cargamos ahora nuestros componentes list desde **main.js**

```
import List from './components/List'
import Detail from './components/Detail'

```

luego crear una instancia de nuestro Vue-router en **main.js**

```
const router = new VueRouter({
  routes // short for `routes: routes`
})
```

y por ulitmo agregar router en new Vue:

```
new Vue({
  **router,**
  render: h => h(App),
}).$mount('#app')

```

# History Mode

para que en las rutas no quede un numeral desagradable

```
const router = new VueRouter({
  mode: 'history',
  routes: [...]
})

```

## Dynamic Route Matching

```
const routes = [
  { path: '/', component: List },
  { path: '/Detail/:id', component: Detail },
]

```

# \***\*\*\*\*\***\*\*\*\*\***\*\*\*\*\***DJANGO****\*\*****\*\*\*\*****\*\*****\*\*****\*\*****\*\*\*\*****\*\*****

# CREAR OTRA APP PARA LOS COMENTARIOS EN NUESTRO PROYECTO DE DJANGO

ejecutamos el siguiente comando dendro de nuestro proyecto **Djangovue**
`python manage.py startapp comment`

luego agregamos nuestra app `comment` en el archivo **settings.py**
`INSTALLED_APPS = [ ....., `comment`] `

## crear el modelo y migracion para la app Comment

vamos al archivo de modelos en **comment/models.py**

```
from django.db import models

# Create your models here.

class Comment(models.Model):
   text = models.TextField()
   data_posted = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       return 'Comentario #{}'.format(self.id)
```

y luego corremos las migraciones con `python manage.py makemigrations` y se crea el
modelo comment y la tabla 0001_initial.py
Luego ejecutamos las migraciones para que crea la base de datos con el comando:
`python manage.py migrate`

luego registramos nuestra app en Admin vamos al achivo de **admin.py**

```
from django.contrib import admin
from .models import Comment
# Register your models here.

admin.site.register(Comment)
```

luego levantamos nuestra app `python manage.py runserver`

## crear un listado de los comentarios

vamos al archivo **comments/views.py**

```
from django.shortcuts import render
from .models import Comment
# Create your views here.

def index(request):
    comments = Comment.objects.all()
    return render(request, 'index.html', {'comments':comments})
```

luego creamos un archivo de rutas para nuestra app **comments/urls.py**

```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

Luego agregamos la ruta de los comments en nuestra app principal
**Djangovue/urls.py**

```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('listelement.urls')),
    **path('comment/', include('comment.urls')),**
]
```

Luego creamos el Temple en nuestra app comments creamos una carpeta template y agregamos el index **comments/templates/index.html** escribimos algo y vamos a chequear en `http://127.0.0.1:8000/comment/`

## Crear un formaulario para agregar comentario

creamos un archivo forms.py **comments/forms.py**

```
from  django.forms import ModelForm
from .models import Comment
class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ("text",)
```

Luego agregamos a nuestro **comments/views.py** el metodo de nuestro forms.py

```
from django.shortcuts import render
from .models import Comment
from .forms import CommentForm
def index(request):
    comments = Comment.objects.all()
    return render(request, 'index.html', {'comments':comments})

def add(request):
    form = CommentForm()

    return render(request, 'add.html', {'from':form})
```

Creamos el siguiente temple de form **comments/templates/add.html** y mostramos el html

```
<body>
    {{ form.text }}
</body>
```

luego creamos la nueva ruta de nuestrs fistas en **comments/urls.py**

```
urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),]
```

## bootstrap-form

es una forma sencilla de css para los forms en Django
`pip install django-bootstrap-form`  
en el html se agrega

```
  {% load static %}
    {% load bootstrap %}

    <link rel="stylesheet" href="{% static 'bootstrap/dist/css/bootstrap.min.css' %}">

<body>
     <div class="container">
        <form action="" method="post">

            {{ form | bootstrap }}

            <input type="submit" value="Enviar">
        </form>
    </div>
```

Luego agregamos en **settings.py** `bootstrap-form`

```
INSTALLED_APPS = [
    .....
    `bootstrapform`
]
```

## Subir archivos en forms

si da error al no subir una imagen se debe instalar el plugin:
`pip install Pillow`

# GUARDAR LA INFORMACION DE CONTACTO EN BASE DE DATOS

primero hay que crear una clase de los campos en la base de datos en **comments/models.py**

```
class Contact(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.CharField(max_length=70)
    phone = models.CharField(max_length=13)
    date_birth = models.DateTimeField()
    documento = models.FileField(upload_to='uploads/contact')
```

luego aplicar `python manage.py makemigrations`
y por ultimo `python manage.py migrate`
esto creara un tabla llamada '**comment_contact**' en la base de datos

#

# MOSTRAS Y MEJORAR TODOS LOS DATOS EN LA API-REST DJANGO

#

**serializer.py**

```
from rest_framework import serializers
from .models import Element, Category, Type
# importamos un modelo de otra aplicacion:
from comment.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # fields = ['text','id'] # para que solo muestre algunos elementos
        fields = '__all__'
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'
class ElementSerializer(serializers.ModelSerializer):
    category =  CategorySerializer(read_only=True)
    type =  TypeSerializer(read_only=True)
    # comments = serializers.StringRelatedField(many=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Element
        fields = '__all__'
```

**viewsets.py**

```
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Element, Category, Type
from django.shortcuts import get_object_or_404
from .serializer import ElementSerializer, CategorySerializer, TypeSerializer, CommentSerializer
from comment.models import Comment

class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all() # devuelve toda la colecion de elementos
    serializer_class = ElementSerializer
# class CategoryViewSet(viewsets.ModelViewSet):
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
# metodos personalizados
    @action(detail=True, methods=['get'])
    def elements(self, request, pk=None):
        queryset = Element.objects.filter(category_id=pk)
        serializer = ElementSerializer(queryset, many=True)
        return Response(serializer.data)
class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    # metodos personalizados
    @action(detail=True, methods=['get'])
    def elements(self, request, pk=None):
        queryset = Element.objects.filter(type_id=pk)
        serializer = ElementSerializer(queryset, many=True)
        return Response(serializer.data)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

```

en **urls.py** agregamos la siguiente ruta

```
from django.urls import path
from rest_framework import routers
from .viewsets import ElementViewSet, CategoryViewSet, TypeViewSet, CommentViewSet
route = routers.SimpleRouter()
route.register('element', ElementViewSet)
route.register('category', CategoryViewSet)
route.register('type', TypeViewSet)
route.register('comment', CommentViewSet)

urlpatterns = route.urls
```

# habilitar paginacion rest api

https://www.django-rest-framework.org/api-guide/pagination/
**settings.py** pegamos en cualquier parte

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100}

```

#

# authentication system DJANGO

#

# https://docs.djangoproject.com/en/3.0/topics/auth/default/

agregamos el siguiente path en en archivo **djangovue/urls.py**

urlpatterns = [
....
`path('accounts/', include('django.contrib.auth.urls')),`
]

creamos una appicacion nueva para llevar mas contros con el nombre `account` con el siguiente comando: `python manage.py startapp account` y luego la agregamos nuestra nueva app en **DjangoVue/settings.py**
INSTALLED_APPS = [
....
'account',
]
luego creamos en carpeta en la app nueva con el nombre de **templates** y movemos nuestra la carpeta **registration** a templates

# CONFIGURACION DE ENVIO DE EMAIL PARA RESET CLAVE

https://www.udemy.com/course/django-3-con-python-3-integracion-con-vue-2-y-bootstrap-4/learn/lecture/18625422#questions
Crear un usuario gratuito en https://mailtrap.io/inboxes para tener el server de coreos y ir a `Demo inbox` y en **Integration** buscamos `Django`
y pegamos nuestras claves en **settings.py** al final de nuestra codigo
EMAIL_HOST = 'smt\***\*\*\*\*\*\*\***'
EMAIL_HOST_USER = '**\*\*\***'
EMAIL_HOST_PASSWORD = '**\***'
EMAIL_PORT = '2525'

# INSTALACION DE PAQUETES PAYPAL

https://developer.paypal.com/docs/api/rest-sdks/#

```
pip install paypalhttp
pip install paypal-checkout-serversdk
```
