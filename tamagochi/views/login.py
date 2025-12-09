from django.shortcuts import render, redirect
from tamagochi.forms import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
import random
from django.utils import timezone
import geocoder
from requests import get
from ipware import get_client_ip


def make_view(request,errors,login_form = LoginForm()):
    context = {'login_form': login_form,'errors':errors}
    print(context['login_form'])
    return render(request, 'authen/login.html', context)


def get_egg(request):
    if 'tname' in request.POST and request.POST['tname']:
        name = request.POST['tname']
        if Tamagochi.objects.filter(name__exact=name):
            return render(request,"authen/egg.html",{'errors':"Your tamagochi's name is taken by somebody else"})
        else:
            ran = random.randint(1, 32)
            if ran % 2 == 0:
                gender = 'Female'
            else:
                gender = 'Male'
            ran = ran.__str__()
            filename = '/tamaEvolve/' + ran + '/1.png'
            log = LoginLogoutLog.objects.get(user=request.user)
            log.length = None
            log.login_time = timezone.now()
            log.save()

            # get ip and latlong
            try:
                ip, is_routable = get_client_ip(request)
                if ip:
                    latlong = get('https://ipapi.co/{}/latlong/'.format(ip)).text.split(',')
                    if len(latlong) == 2 and latlong[0] != 'Undefined':
                        latitude = latlong[0]
                        longitude = latlong[1]
                    else:
                        # Default location: Pittsburgh, PA (based on README)
                        latitude = '40.4406'
                        longitude = '-79.9959'
                else:
                    # Default location: Pittsburgh, PA
                    latitude = '40.4406'
                    longitude = '-79.9959'
            except Exception as e:
                print(f"Geolocation error: {e}")
                # Default location: Pittsburgh, PA
                latitude = '40.4406'
                longitude = '-79.9959'

            new_tamagochi = Tamagochi(name=name,user=request.user, gender=gender,apperance=filename
                                      ,apperanceNum=ran,online=True,latitude=latitude,longitude=longitude)
            new_tamagochi.save()
            return redirect('map')
    else:
        return render(request,"authen/egg.html",{})


def login_view(request):
    errors = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        errors.append('no such username.')
        if form.is_valid():
            user = authenticate(request,username=form.cleaned_data['username'],password=form.cleaned_data['password'])

            if user is not None:
                auth_login(request, user)

                if LoginLogoutLog.objects.filter(user=user).exists():
                    log = LoginLogoutLog.objects.get(user=user)
                    log.login_time = timezone.now()
                    log.save()
                else:
                    log = LoginLogoutLog(user=user)
                    log.login_time = timezone.now()
                    log.save()
                try:
                    pet_self = Tamagochi.objects.get(user=user)
                    pet_self.online=True

                    # get ip and latlong
                    try:
                        ip, is_routable = get_client_ip(request)
                        if ip:
                            latlong = get('https://ipapi.co/{}/latlong/'.format(ip)).text.split(',')
                            if len(latlong) == 2 and latlong[0] != 'Undefined':
                                pet_self.latitude = latlong[0]
                                pet_self.longitude = latlong[1]
                            else:
                                # Default location: Pittsburgh, PA
                                pet_self.latitude = '40.4406'
                                pet_self.longitude = '-79.9959'
                        else:
                            # Default location: Pittsburgh, PA
                            pet_self.latitude = '40.4406'
                            pet_self.longitude = '-79.9959'
                    except Exception as e:
                        print(f"Geolocation error: {e}")
                        # Default location: Pittsburgh, PA
                        pet_self.latitude = '40.4406'
                        pet_self.longitude = '-79.9959'
                    pet_self.save()
                    return redirect('map')
                except:
                    return get_egg(request)
            else:
                errors.pop()
                errors.append('User and password do not match.')
    else:
        form=LoginForm()
    return render(request,'authen/login.html',{'form':form,'errors':errors})
