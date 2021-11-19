from django import forms
from .cipher_classes.vigenere import VigenereCipher
from .cipher_classes.rsa import RSACipher
from . import constants
import re


class VigenereForm(forms.Form):
    cipher = VigenereCipher()
    key = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    decrypted_text = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    encrypted_text = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        if 'encrypt' in self.data:
            valid_chars_in_fields(self, ['key', 'decrypted_text'])
            fields_required(self, ['key', 'decrypted_text'], "This field is required when encrypting.")
        elif 'decrypt' in self.data:
            valid_chars_in_fields(self, ['key', 'encrypted_text'])
            fields_required(self, ['key', 'encrypted_text'], "This field is required when decrypting.")
        else:
            self.add_error('', "Missing submit type")
        return cleaned_data


class DESForm(forms.Form):
    key = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    CHOICES = [('text', 'Text Input'),
               ('file', 'File Input')]
    input_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    decrypted_text = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '5',
                                                                              'class': 'form-control'}))
    decrypted_file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    encrypted_text = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '5',
                                                                              'class': 'form-control'}))
    encrypted_file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        input_type = cleaned_data.get('input_type', 'text')
        if 'encrypt' in self.data:
            fields_required(self, ['key', f'decrypted_{input_type}'], "This field is required when encrypting.")
        elif 'decrypt' in self.data:
            fields_required(self, ['key', f'encrypted_{input_type}'], "This field is required when decrypting.")
        elif 'generate_key' in self.data:
            pass
        else:
            pass
        return cleaned_data


class RSAForm(forms.Form):
    cipher = RSACipher()
    public_key = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    private_key = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    decrypted_text = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    encrypted_text = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        if 'encrypt' in self.data:
            fields_required(self, ['public_key', 'decrypted_text'], "This field is required when encrypting.")
        elif 'decrypt' in self.data:
            fields_required(self, ['private_key', 'encrypted_text'], "This field is required when decrypting.")
        elif 'generate_keys' in self.data:
            pass
        else:
            self.add_error('', "Missing submit type")
        valid_chars_in_fields(self,
                              ['public_key', 'private_key'],
                              message="This field contains invalid characters. Only 0-9 and , are allowed.",
                              characters='0-9,')
        return cleaned_data


class MD5Form(forms.Form):
    CHOICES = [('text', 'Text Input'),
               ('file', 'File Input')]
    input_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    input_text = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '4',
                                                                              'class': 'form-control'}))
    input_file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    output_hash = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '2',
                                                                               'class': 'form-control',
                                                                               'readonly': 'readonly'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        if self.data.get('hash'):
            input_type = cleaned_data.get('input_type', 'text')
            fields_required(self, [f'input_{input_type}'], "This field is required when hashing.")
            if input_type == 'text':
                print('temp text')
            elif input_type == 'file':
                print('temp file)')
            else:
                self.add_error('', "At least one input field must be filled out.")
        return cleaned_data


def fields_required(form, fields, message="This field is required."):
    for field in fields:
        if not form.cleaned_data.get(field, ''):
            msg = forms.ValidationError(message)
            form.add_error(field, msg)
            form.fields[field].widget.attrs['class'] += ' is-invalid'


def valid_chars_in_fields(form, fields, message="This field contains invalid characters.", characters=' -~\t\r\n'):
    pattern = re.compile('^[' + characters + ']+$')
    for field in fields:
        contents = form.cleaned_data.get(field, '')
        if contents:
            if not re.search(pattern, contents):
                msg = forms.ValidationError(message)
                form.add_error(field, msg)
                form.fields[field].widget.attrs['class'] += ' is-invalid'

