from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ListifyForm
from .models import Listify
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        return redirect('currentnotes')
    else:
        return render(request, 'listapp/home.html')


#Auth
def signupuser(request):
    if request.user.is_authenticated:
        return redirect('currentnotes')
    if request.method == 'GET':
        return render(request, 'listapp/signupuser.html',
                      {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentnotes')
            except IntegrityError:
                return render(
                    request, 'listapp/signupuser.html', {
                        'form':
                        UserCreationForm(),
                        'error':
                        'That username has already been taken. Please choose a new username'
                    })
        else:
            return render(request, 'listapp/signupuser.html', {
                'form': UserCreationForm(),
                'error': 'Invalid username or password.'
            })


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('currentnotes')
    if request.method == 'GET':
        return render(request, 'listapp/loginuser.html',
                      {'form': AuthenticationForm()})
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(
                request, 'listapp/loginuser.html', {
                    'form': AuthenticationForm(),
                    'error': 'Invalid username or password.'
                })
        else:
            login(request, user)
            return redirect('currentnotes')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


#Listify

@login_required
def createnote(request):
    if request.method == 'GET':
        return render(request, 'listapp/createnote.html',
                      {'form': ListifyForm()})
    else:
        try:
            form = ListifyForm(request.POST)
            newnote = form.save(commit=False)
            newnote.user = request.user
            newnote.save()
            return redirect('currentnotes')
        except ValueError:
            return render(request, 'listapp/createnote.html',
                          {'form': ListifyForm()},
                          {'error': 'Bad data passed in. Try again'})


@login_required
def currentnotes(request):
    notes = Listify.objects.filter(user=request.user,
                                   datecompleted__isnull=True)
    return render(request, 'listapp/currentnotes.html', {'notes': notes})


@login_required
def completednotes(request):
    notes = Listify.objects.filter(
        user=request.user,
        datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'listapp/completednotes.html', {'notes': notes})


@login_required
def viewnote(request, note_pk):
    note = get_object_or_404(Listify, pk=note_pk, user=request.user)
    if request.method == 'GET':
        form = ListifyForm(instance=note)
        return render(request, 'listapp/viewnote.html', {
            'note': note,
            'form': form
        })
    else:
        try:
            form = ListifyForm(request.POST, instance=note)
            form.save()
            return redirect('currentnotes')
        except ValueError:
            return render(request, 'listapp/viewnote.html', {
                'note': note,
                'form': form
            }, {'error': 'Bad info'})


@login_required
def completenote(request, note_pk):
    note = get_object_or_404(Listify, pk=note_pk, user=request.user)
    if request.method == 'POST':
        note.datecompleted = timezone.now()
        note.save()
        return redirect('currentnotes')


@login_required
def deletenote(request, note_pk):
    note = get_object_or_404(Listify, pk=note_pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('currentnotes')
