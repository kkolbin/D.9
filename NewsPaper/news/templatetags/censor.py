from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='censor')
def censor(value):
    censored_words = ['питание', 'закаливание', ...]  # список нежелательных слов

    words = value.split()  # разделение строки на отдельные слова

    censored_words_count = 0  # счетчик количества удаленных слов

    for i in range(len(words)):
        if words[i] in censored_words:
            words[i] = '*' * len(words[i])  # замена нежелательного слова на звездочки
            censored_words_count += 1

    censored_value = ' '.join(words)  # объединение слов обратно в строку
    return mark_safe(censored_value)