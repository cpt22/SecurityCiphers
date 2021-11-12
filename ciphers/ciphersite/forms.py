from django import forms
from .cipher_classes.vigenere import VigenereCipher


class VigenereForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(self, *args, **kwargs)
    #     self.cipher = VigenereCipher()
    cipher = VigenereCipher()
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


def fields_required(form, fields, message="This field is required."):
    for field in fields:
        if not form.cleaned_data.get(field, ''):
            msg = forms.ValidationError(message)
            form.add_error(field, msg)
            form.fields[field].widget.attrs['class'] += ' is-invalid'

