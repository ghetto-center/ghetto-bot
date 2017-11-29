#! /usr/bin/env python3

import sys
import re
import random
import pymorphy2
import pymorphy2.tokenizers
import pymorphy2.shapes

morph = pymorphy2.MorphAnalyzer()

def get_parsed_words(phrase):
    tokens = pymorphy2.tokenizers.simple_word_tokenize(phrase)
    words = [t for t in tokens if (morph.word_is_known(t) and not pymorphy2.shapes.is_punctuation(t))]
    parsed_words = [morph.parse(word)[0] for word in words]
    return filter(None, parsed_words)

def is_verb(parsed):
    return 'VERB' in parsed.tag or 'INFN' in parsed.tag

def remove_refl(parsed):
    """
    Пытается убрать возвратную форму глагола
    """
    not_refl = re.sub('ся$', '', parsed.normal_form)

    if not morph.word_is_known(not_refl):
        return parsed
    else:
        return morph.parse(not_refl)[0]

def anus(input):
    parsed_words = get_parsed_words(input)
    verbs = [
        remove_refl(p).inflect({'sing','impr','excl'})
        for p in parsed_words
        if is_verb(p)
    ]

    verbs = list(filter(None, verbs))

    if verbs:
        return 'Анус себе ' + verbs[-1].word

    return None

def mamka(input):
    parsed_words = get_parsed_words(input)
    verbs = [
        remove_refl(p).inflect({'past', 'sing', 'masc'})
        for p in parsed_words
        if is_verb(p)
    ]

    verbs = list(filter(None, verbs))

    if verbs:
        return 'Вчера мамку твою ' + verbs[-1].word

    return None


def random_joke(input):
    joke_fn = random.choice([anus, mamka])
    return joke_fn(input)

if __name__ == '__main__':
    input = sys.argv[1]
    ghettodev_joke = random_joke(input)
    print(ghettodev_joke or 'Чо?')
