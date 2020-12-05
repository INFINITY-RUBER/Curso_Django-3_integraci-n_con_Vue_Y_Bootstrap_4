from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth.hashers  import check_password

# Create your views here.

@api_view(['POST'])
def login(request):

    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response('Usuario invalido')

    pwd_valid = check_password(password, user.password)

    if not pwd_valid:
        return Response('Contraseña invalida')


    token, _ = Token.objects.get_or_create(user=user)

    print(token.key)
    return Response(token.key)