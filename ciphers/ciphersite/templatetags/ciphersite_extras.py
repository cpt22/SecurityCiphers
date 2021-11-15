from django.template.defaulttags import register


@register.filter
def get_field_data(form, key):
    if hasattr(form, 'cleaned_data') and key in form.cleaned_data:
        return form.cleaned_data.get(key, '')
    elif hasattr(form, 'data') and key in form.data:
        return form.data.get(key, '')
    return ''

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def break_join(lis):
    return '<br>'.join(lis)
