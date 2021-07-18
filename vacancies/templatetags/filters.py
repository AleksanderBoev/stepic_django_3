from django import template

register = template.Library()


@register.filter(name='null_to_no')
def null_to_no(value):
    if str(value) == '0':
        return 'нет'
    return value

@register.filter(name='rus_plural_endings')
def rus_plural_endings(value, arg):
    if 5 <= abs(value) % 100 <= 20 or value == 0:
        print('ий')
        return arg + 'ий'
    if abs(value) % 10 == 1:
        print('ия')
        return arg+'ия'
    if 2 <= abs(value) % 10 <= 4:
        print('ии')
        return arg + 'ии'
