#! /usr/bin/env python3

import sys
import re
import random
import pymorphy2
import pymorphy2.tokenizers
import pymorphy2.shapes
from joke_utils import rnd_percent

morph = pymorphy2.MorphAnalyzer()

REPLAY_STICKERS = [
    # Philosophy_Guys
    'CAADAgADOwADI0MjBN4jX02o9zbkAg',
    'CAADAgADTQADI0MjBOI8uXDt5018Ag',
    'CAADAgADUwADI0MjBI9qdrfse_1KAg',
    'CAADAgADXwADI0MjBCWzG9qbeQ0qAg',
    'CAADAgADYQADI0MjBAiuQ2UstpRqAg',
    'CAADAgADZQADI0MjBA1fm14ELL2NAg',
    # Otbitye
    'CAADAgADpgAD8MPADv8UZs0RBe8_Ag',
    # teadosug
    'CAADAgADHgIAAqtWmgyIVOr0Kow7FwI',
    'CAADAgADhgMAAqtWmgy3OXs8A3yWngI',
    # MisanthropePack
    'CAADAgADxAAD0MeAA28XQId4qd4SAg',
    'CAADAgADngAD0MeAA3YXoY7wEYayAg',
    # Otbitye
    'CAADAgADtwAD8MPADnKh2YgsemeKAg',
    'CAADAgADsQAD8MPADjnqHSIZisRyAg',
    'CAADAgADlQAD8MPADkzhLTh5l5SNAg',
    'CAADAgADTAAD8MPADuytjq92fqZCAg',
    'CAADAgADwQAD8MPADtHSHJUvOj69Ag',
    'CAADAgADgQAD8MPADj1a4tbu0ojpAg',
    'CAADAgAD2wAD8MPADtV_3subekgpAg',
]

STICKERS = [
    # CuteRude
    'CAADAgADpQEAAmX_kgpp3dwbGB2UzQI',
    'CAADAgADpgEAAmX_kgqaHEalGW2KAQI',
    'CAADAgADqAEAAmX_kgrZcgEWrTPlDQI',
    'CAADAgADpwEAAmX_kgqQSQ24CtKgRQI',
    'CAADAgADswEAAmX_kgqA89pR_ckRcgI',
    'CAADAgADtQEAAmX_kgoceL-VX5Xs9gI',
    'CAADAgADtgEAAmX_kgrDvtRbdN-T7gI',
    # futurama_pouyasaadeghi
    'CAADBAADEQADmDVxAkmg3XnDZam0Ag',
    'CAADBAADEwADmDVxAp3k1xTFyNcyAg',
    'CAADBAADFwADmDVxAk8LCwZgEU7kAg',
    'CAADBAADGwADmDVxApFTHg4W1PB8Ag',
    'CAADBAADHwADmDVxAsVMpnbj30pPAg',
    'CAADBAADIQADmDVxAkNQwGGebphEAg',
    'CAADBAADJwADmDVxAguchI9CI5-dAg',
    'CAADBAADKwADmDVxAmIdrKk5BjVdAg'
    # teadosug
    'CAADAgAD_AIAAqtWmgxuTuKES-CnfAI',
    # MisanthropePack
    'CAADAgADpAAD0MeAA5LOnR08iFEYAg',
]

JOKES = [
    'Ребята, может на го всё перепишем?',
    'Как дела? Проблемы какие?',
    'Надо пойти в стандарт бар.',
    'Не пора ли нам в кальянную?',
    'Спинер крутится, сайты мутятся!',
    'Ублюдок, мать твою, а ну иди сюда, говно собачье! A? Что, решил ко мне лезть?! Ты, засранец вонючий, мать твою, а? Ну, иди сюда, попробуй меня трахнуть, я тебя сам трахну, ублюдок, онанист чертов, будь ты проклят! Иди, идиот, трахать тебя и всю твою семью, говно собачье, жлоб вонючий, дерьмо, сука, падла! Иди сюда, мерзавец, негодяй, гад, иди сюда, ты, говно, ЖОПА!'
]


def dict_joke():
    return random.choice(JOKES)


def sticker_id():
    return random.choice(STICKERS)


def reply_sticker_id():
    return random.choice(REPLAY_STICKERS)


def get_parsed_words(phrase):
    tokens = pymorphy2.tokenizers.simple_word_tokenize(phrase)
    words = [t for t in tokens if (morph.word_is_known(
        t) and not pymorphy2.shapes.is_punctuation(t))]
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


def joke_base(input, phrase, inflection):
    parsed_words = get_parsed_words(input)
    verbs = [
        remove_refl(p).inflect(inflection)
        for p in parsed_words
        if is_verb(p)
    ]

    verbs = list(filter(None, verbs))

    if verbs:
        return phrase.format(verbs[-1].word)

    return None


def anus_rude(input):
    return joke_base(input, 'Анус себе {}, пес', {'sing', 'impr', 'excl'})


def anus(input):
    return joke_base(input, 'Анус себе {}', {'sing', 'impr', 'excl'})


def mamka(input):
    return joke_base(input, 'Вчера мамку твою {}', {'past', 'sing', 'masc'})


def how_you_doing(input, phrase):
    match = re.search('\s*как\s+сам(-то)?\s*(\?|$)', input, re.I)
    if match:
        return random.choice(phrase)
    return None


def is_good(input):
    parsed_words = get_parsed_words(input)
    good = False
    for p in parsed_words:
        if p.normal_form in ['мамка', 'мамаша', 'мама', 'мать', 'анус']:
            good = True
            break
    return good


def is_plan(input):
    parsed_words = get_parsed_words(input)
    plan = False
    for p in parsed_words:
        if 'VERB' in p.tag and 'futr' in p.tag and 'indc' in p.tag:
            plan = True
            break
    return plan


def good_job(input):
    if is_good(input) and rnd_percent(20):
        return 'А ты хорош!'
    return None


def looks_like_plan(input):
    if is_plan(input) and rnd_percent(5):
        return 'Звучит как план!'
    return None


def fag_reply(input):
    match = re.search('\s*[HН]\s*[EЕ]\s*[TТ]\s*([?!.]+)?\s*$', input, re.I)
    if match:
        return 'Пидора ответ!'
    return None


def regex_joke(input):
    return how_you_doing(input, ['Как сала килограмм!', 'Как пустой универсам!']) or fag_reply(input) or good_job(
        input) or looks_like_plan(input)


def random_joke(input):
    joke_fn = random.choice([anus, mamka, anus_rude])
    return joke_fn(input)


if __name__ == '__main__':
    input = sys.argv[1]
    ghettodev_joke = random_joke(input)
    print(ghettodev_joke or 'Чо?')
