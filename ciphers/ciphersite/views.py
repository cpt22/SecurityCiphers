import hashlib
import hmac
import json
import subprocess
from ciphers import settings
from decouple import config
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .forms import VigenereForm, DESForm, MD5Form, RSAForm


def index(request):
    context = {}
    return render(request, 'ciphersite/index.html', context)


def vigenere(request):
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
    #if request.method == 'POST':
    #else:
    form = DESForm({'input_type': 'text'})

    context = {'form': form}
    return render(request, 'ciphersite/des.html', context)


def rsa(request):
    if request.method == 'POST':
        vals = request.POST
        form = RSAForm(vals)
        if form.is_valid():
            if 'generate_keys' in vals:
                private_key, public_key = form.cipher.generate_keys()
                print(private_key)
                print(public_key)
                form.cleaned_data['private_key'] = f"{private_key[0]},{private_key[1]}"
                form.cleaned_data['public_key'] = f"{public_key[0]},{public_key[1]}"
            elif 'encrypt' in vals:
                key_parts = [int(x.strip()) for x in form.cleaned_data['public_key'].split(',')]
                ciphertext = form.cipher.encrypt(str.encode(form.cleaned_data['decrypted_text']), key_parts)
                form.cleaned_data['encrypted_text'] = ciphertext
            elif 'decrypt' in vals:
                key_parts = [int(x.strip()) for x in form.cleaned_data['private_key'].split(',')]
                ciphertext = form.cipher.decrypt(str.encode(form.cleaned_data['encrypted_text']), key_parts)
                form.cleaned_data['decrypted_text'] = ciphertext
    else:
        form = RSAForm()
    context = {'form': form}
    return render(request, 'ciphersite/rsa.html', context)


def md5(request):
    if request.method == 'POST':
        form = MD5Form(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data.get('input_text'):
                print(str.encode(form.cleaned_data.get('input_text')))
            elif form.cleaned_data.get('input_file'):
                print(request.FILES.get('input_file').read())
            else:
                return HttpResponse('Invalid Request', status=400)
    else:
        form = MD5Form({'input_type': 'text'})

    context = {'form': form}
    return render(request, 'ciphersite/md5.html', context)


@csrf_exempt
def ci(request):
    headers = request.headers
    if any(header not in headers.keys() for header in ['X-Hub-Signature', 'X-Github-Event']):
        return HttpResponse('Invalid Request', status=400)

    secret = config('WEBHOOK_SECRET')
    git_signature = headers.get('X-Hub-Signature').replace("sha1=", "")
    signature = hmac.new(secret.encode(), request.body, hashlib.sha1)
    expected_signature = signature.hexdigest()
    if not hmac.compare_digest(git_signature, expected_signature):
        return HttpResponseForbidden('Invalid signature header')

    event_type = headers["X-Github-Event"]
    obj = json.loads(request.body)
    if event_type == 'push':
        valid_branches_for_push = ['master']
        ref = obj.get('ref')
        if any(branch in ref for branch in valid_branches_for_push):
            commits = obj.get('commits')
            if commits:
                num_commits = str(len(commits))
                subprocess.Popen([f"{str(settings.BASE_DIR)}/post-receive.sh", num_commits, ref])
                return HttpResponse(f"Successfully landed {num_commits} commits on {ref}")
            else:
                return HttpResponse(f"No commits to land on {ref}")
        else:
            return HttpResponse(f"This server does not support landing commits from {ref}")

    return HttpResponse("Request was validated, but this event is not handled by the server")
