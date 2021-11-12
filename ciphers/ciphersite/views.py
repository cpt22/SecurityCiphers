from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import VigenereForm


def index(request):
    context = {}
    return render(request, 'ciphersite/index.html', context)


def vigenere(request):
    form = None
    if request.method == 'POST':
        vals = request.POST
        form = VigenereForm(vals)
        if form.is_valid():
            if 'encrypt' in vals:
                print(form.cipher.encrypt(form.cleaned_data['key'], form.cleaned_data['decrypted_text']))
            elif 'decrypt' in vals:
                print(form.cipher.decrypt(form.cleaned_data['key'], form.cleaned_data['encrypted_text']))
    else:
        form = VigenereForm()

    context = {'form': form}
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