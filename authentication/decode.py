import os
from base64 import b64decode
from itsdangerous import base64_decode
import zlib
import json
import re

def decode(cookie):
    """Decode a Flask cookie."""
    try:
        compressed = False
        payload = cookie

        if payload.startswith('.'):
            compressed = True
            payload = payload[1:]

        data = payload.split(".")[0]

        data = base64_decode(data)
        if compressed:
            data = zlib.decompress(data)

        return data.decode("utf-8")
    except Exception as e:
        return "[Decoding error: are you sure this was a Flask session cookie? {}]".format(e)

def extract_session(txt):
    m = re.search(r"session=(.*)", txt)
    if m:
        return m.group(1)
