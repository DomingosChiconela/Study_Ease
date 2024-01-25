from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import constants
from django.contrib import messages

from django.contrib import auth




def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(
                request, constants.ERROR, 'As senhas não coincídem'
            )
            return redirect(reverse('cadastro'))

        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(
                request,
                constants.ERROR,
                'Já existe um usuário com o mesmo username',
            )
            return redirect(reverse('cadastro'))

        try:
            user = User.objects.create_user(
                username=username,
                password=confirmar_senha,
            )
            messages.add_message(
                request, constants.SUCCESS, 'Usuário cadastrado com sucesso.'
            )
            return redirect(reverse('login'))
        except:
            messages.add_message(
                request, constants.ERROR, 'Erro interno do sistema'
            )
            return redirect(reverse('cadastro'))
        
        
def logar(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username=username, password=senha)
      
        if user:
            auth.login(request, user)
            
            messages.add_message(request, constants.SUCCESS, 'Logado!')
            return redirect('/flashcard/novo_flashcard/')
        else:
            messages.add_message(
                request, constants.ERROR, 'Username ou senha inválidos'
            )
            return redirect(reverse('login'))
        
        
def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))