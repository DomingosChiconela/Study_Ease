from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.urls import reverse
from . models import Apostila,ViewApostila




def adicionar_apostilas(request):
    if request.method == 'GET':
        apostilas = Apostila.objects.filter(user=request.user)
      
        totalviews =  ViewApostila.objects.filter(apostila__user=request.user).count()  
        print(totalviews)
        return render(request, 'adicionar_apostilas.html', {'apostilas': apostilas,'totalviews': totalviews})
    
    elif request.method == 'POST':
        titulo= request.POST.get('titulo')
        arquivo= request.FILES.get('arquivo')
        
        apostila = Apostila(
            user=request.user,
            titulo=titulo,
            arquivo=arquivo
        )
        
        apostila.save()
        
        messages.add_message(request,constants.SUCCESS,'Apostila cadastrada com sucesso')
        
        return redirect(reverse('adicionar_apostilas'))



def apostila(request, id):
    apostila = Apostila.objects.get(id=id)
    
    
    views_unicas = ViewApostila.objects.filter(apostila=apostila).values('ip').distinct().count()
    views_totais = ViewApostila.objects.filter(apostila=apostila).count()
    view=ViewApostila(
        ip=request.META['REMOTE_ADDR'],
        apostila=apostila
            
    )
    view.save()

    return render(request, 'apostila.html', {'apostila': apostila,'views_unicas': views_unicas, 'views_totais':  views_totais  })