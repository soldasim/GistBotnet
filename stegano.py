import base64
import secretpy
import urllib.parse

INITIALIZED = False
CIPHER = secretpy.Vigenere()
BASE_URL = ''
KEY = ''
ALPHABET = secretpy.alphabets.DECIMAL + secretpy.alphabets.ENGLISH + secretpy.alphabets.ENGLISH.upper()


def init_config(config):
    global BASE_URL, KEY
    BASE_URL = config['STEG_URL']
    KEY = config['STEG_KEY']

    global INITIALIZED
    INITIALIZED = True


# TODO: less suspicious message
def ensteg(msg):
    assert INITIALIZED

    url = msg_to_url(msg)
    comment = '[test](' + BASE_URL + '/#' + url + ')'
    return comment


def desteg(comment):
    assert INITIALIZED

    begin = comment.find(BASE_URL) + len(BASE_URL) + 2
    end = comment.find(')', begin)
    url = comment[begin:end]
    msg = url_to_msg(url)
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
