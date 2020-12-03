import os
from django.conf import settings

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as make_login
from django.core.exceptions import ObjectDoesNotExist

from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile

# Create your views here.

def user_data(request):
    # print(request.user.username)
    return render(request,'user_data.html')

@login_required
def profile(request):
    # print(request.user.id)
    form = UserProfileForm()
    if request.method == 'POST':
        pathOlAvatar = None
        try:
            userprofile = UserProfile.objects.get(user=request.user)  
            form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
            
            pathOlAvatar = os.path.join(settings.MEDIA_ROOT,userprofile.avatar.name)
            print(pathOlAvatar)

        except ObjectDoesNotExist:
            form = UserProfileForm(request.POST, request.FILES)


        if form.is_valid():
            if pathOlAvatar is not None and os.path.isfile(pathOlAvatar):
                print('Se borro:', pathOlAvatar)
                os.remove(pathOlAvatar)

            userprofile = form.save(commit=False)
            userprofile.user = request.user
            userprofile.save()
    
    return render(request,'profile.html', {'form':form})
    
def register(request):
    form = CustomUserCreationForm()
    # return redirect(reverse('login'))


    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                make_login(request, user)
                return redirect(reverse('account:profile'))
            # return redirect(reverse('account:profile'))

    return render(request,'register.html',{'form':form})