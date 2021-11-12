import hashlib
import hmac
import json
import subprocess
from decouple import config
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .forms import VigenereForm, MD5Form



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
                ciphertext = form.cipher.encrypt(form.cleaned_data['key'], form.cleaned_data['decrypted_text'])
                form.cleaned_data['encrypted_text'] = ciphertext
            elif 'decrypt' in vals:
                ciphertext = form.cipher.decrypt(form.cleaned_data['key'], form.cleaned_data['encrypted_text'])
                form.cleaned_data['decrypted_text'] = ciphertext
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
    form = None
    if request.method == 'POST':
        form = MD5Form(request.POST, request.FILES)
        if form.is_valid():
            print("Valid form")
    else:
        form = MD5Form()

    context = {'form': form}
    return render(request, 'ciphersite/md5.html', context)


@csrf_exempt
def ci(request):
    secret = config('WEBHOOK_SECRET')
    git_signature = request.META.get('HTTP_X_SIGNATURE')
    signature = hmac.new(secret.encode(), request.body, hashlib.sha1)
    expected_signature = signature.hexdigest()
    if not hmac.compare_digest(git_signature, expected_signature):
        return HttpResponseForbidden('Invalid signature header')

    request_body = json.loads(request.body)
    subprocess.call(['bash', '../post-receive.sh'])
    return HttpResponse(status=200)
