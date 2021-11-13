from django import forms
from .cipher_classes.vigenere import VigenereCipher
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
    decrypted_text = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    encrypted_text = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        if 'encrypt' in self.data:
            fields_required(self, ['key', 'decrypted_text'], "This field is required when encrypting.")
        elif 'decrypt' in self.data:
            fields_required(self, ['key', 'encrypted_text'], "This field is required when decrypting.")
        else:
            self.add_error('', "Missing submit type")
        return cleaned_data


class RSAForm(forms.Form):
    key = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    decrypted_text = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    encrypted_text = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        if 'encrypt' in self.data:
            fields_required(self, ['key', 'decrypted_text'], "This field is required when encrypting.")
        elif 'decrypt' in self.data:
            fields_required(self, ['key', 'encrypted_text'], "This field is required when decrypting.")
        else:
            self.add_error('', "Missing submit type")
        return cleaned_data


class MD5Form(forms.Form):
    input_text = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '4',
                                                                              'class': 'form-control'}))
    input_file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    output_hash = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '2',
                                                                               'class': 'form-control',
                                                                               'readonly': 'readonly'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('input_text', ''):
            pass
        elif cleaned_data.get('input_file') is not None:
            pass
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

