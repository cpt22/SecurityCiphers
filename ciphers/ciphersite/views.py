from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    context = {}
    return render(request, 'ciphersite/index.html', context)


def vigenere(request):
    context = {}
    return render(request, 'ciphersite/vigenere.html', context)


def des(request):
    context = {}
    return render(request, 'ciphersite/des.html', context)


def rsa(request):
    context = {}
    return render(request, 'ciphersite/rsa.html', context)


def md5(request):
    context = {}
    return render(request, 'ciphersite/md5.html', context)