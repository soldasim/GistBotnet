import base64
import secretpy
import urllib.parse
import json
from enum import Enum
import random
import re
import utils

INITIALIZED = False
CIPHER = secretpy.Vigenere()
KEY = ''
ALPHABET = secretpy.alphabets.DECIMAL + secretpy.alphabets.ENGLISH + secretpy.alphabets.ENGLISH.upper() + '+/='


def init_config(config):
    global KEY
    KEY = config['STEG_KEY']

    global INITIALIZED
    INITIALIZED = True


def ensteg(msg):
    assert INITIALIZED

    msgurl = msg_to_url(msg)

    deck = random.choice(list(Deck))
    cardname, carduri = get_random_card(deck)
    note = get_random_note(deck)

    comment = note + '\n' + '[' + cardname +'](' + carduri + '/#' + msgurl + ')'
    return comment


# Returns an empty string if the comment does not contain a hidden message.
def desteg(comment):
    assert INITIALIZED

    uri = re.search('\[.+\](.+/#.+)', comment).group()
    msgurl = uri[uri.rfind('/#')+2:-1]
    
    msg = url_to_msg(msgurl)
    return msg


def msg_to_url(msg):
    msg = text_to_base64(msg)
    msg = CIPHER.encrypt(msg, KEY, ALPHABET)
    msg = urllib.parse.quote_plus(msg)
    return msg


def url_to_msg(url):
    url = urllib.parse.unquote_plus(url)
    url = CIPHER.decrypt(url, KEY, ALPHABET)
    url = base64_to_text(url)
    return url


def text_to_base64(s):
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')


def base64_to_text(b):
    return base64.b64decode(b.encode('utf-8')).decode('utf-8')


# - - - Scryfall Queries - - - - -

class Deck(Enum):
    IZZET = 1
    GRIXIS = 2
    DRAGONS = 3
    AZOR = 4
    KARADOR = 5
    MONORED = 6

QUERIES = {
    Deck.IZZET: 'q=commander%3AUR+AND+%28taggertag%3Asynergy-instants+OR+oracletag%3Asynergy-sorcery+OR+oracletag%3Asynergy-token-creature%29&unique=cards',
    Deck.GRIXIS: 'q=commander%3AUBR+AND+%28%28oracletag%3Adraw-matters+OR+oracletag%3Adiscard-matters%29+OR+%28oracletag%3Areanimate-from-any+OR+oracletag%3Areanimate-from-opponent%29%29&unique=cards',
    Deck.DRAGONS: 'q=commander%3AURG+AND+%28oracletag%3Atribal-dragon+OR+%28oracletag%3Acheat-into-play+AND+oracle%3Acreature%29%29&unique=cards',
    Deck.AZOR: 'q=commander%3AWU+AND+%28oracle%3A"top+of+your+library"+OR+oracletag%3Asynergy-noncreature%29&unique=cards',
    Deck.KARADOR: 'q=commander%3AWBG+AND+%28oracletag%3Areanimate-creature+OR+%28type%3Acreature+AND+%28oracle%3A"when+~+enters+the+battlefield"+OR+oracle%3A"when+~+dies"%29%29%29&unique=cards',
    Deck.MONORED: 'q=commander%3AR+AND+%28oracletag%3Acheat-into-play+OR+%28type%3Acreature+cmc%3E5+%28rarity%3Ar+OR+rarity%3Am%29%29%29&unique=cards'
}

NAMES = {
    Deck.IZZET: ['izzet', 'izzet deck', 'Zaffai deck', 'spellslinger deck'],
    Deck.GRIXIS: ['grixis', 'grixis deck', 'Abaddon deck'],
    Deck.DRAGONS: ['dragon deck', 'dragons', 'temur dragon deck'],
    Deck.AZOR: ['azorius', 'azorius deck', 'Tameshi deck', 'artifact/enchantment deck'],
    Deck.KARADOR: ['Karador', 'Karador deck', 'abzan reanimator deck'],
    Deck.MONORED: ['monored', 'monored deck', 'Ilharg deck', 'red deck', 'red aggro deck']
}

NOTES = [
    ("A cool card for my ", " :)"),
    ("consider for ", ""),
    ("", " ?"),
    ("maybe ", ""),
    ("could be good in ", ""),
    ("Nice card for ", " :)"),
    ("my ", " needs this!"),
    ("wow, what a card!\nput in ", ""),
    ("might be good in ", "? not sure"),
    ("buy this. great in ", ""),
    ("cool & underrated, synergy with ", ""),
    ("great synergy with my ", ""),
    ("", ""),
    ("BUYLIST: ", "")
]


def get_random_card(deck):
    res = utils.perform_command("curl https://api.scryfall.com/cards/random?" + QUERIES[deck])
    data = json.loads(res)
    
    name = data['name']

    uri = data['scryfall_uri']
    uri = uri[:uri.rfind('?')]

    return name, uri


def get_random_note(deck):
    begin, end = random.choice(NOTES)
    deckname = random.choice(NAMES[deck])
    return begin + deckname + end
