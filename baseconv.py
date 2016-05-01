#! /usr/bin/env python3

import json

from flask import Flask
from flask import request
app = Flask(__name__)

errcodes = {
    0: 'success',
    404: 'try /0o144 , /0xdeadbeef, /0b1100100, /42. optionally, use ?pad. source: git.io/baseconv',
    'parseerror': 'parse error!'
}

class Response:
    def __init__(self, errcode, _binary = None, _oct = None, _dec = None, _hex = None):
        self.status = errcode;
        if (errcode == 0):
            self._binary = _binary;
            self._oct    = _oct;
            self._dec    = _dec;
            self._hex    = _hex;
        else:
            self.errmessage = errcodes[errcode];

    # http://stackoverflow.com/a/15538391
    def to_JSON(self):
        return '<pre>' + json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4) + '</pre>'

def padnsplit(s, n):
    return ( " ".join([s[k:k+n].zfill(n) for k in range(0, len(s), n)]) )

@app.route('/')
def hello_world():
    return Response(404).to_JSON();

@app.route('/<a>')
def baseconv(a):
    try:
        _from = int(a, 0)
    except:
        return Response('parseerror').to_JSON();

    _bin = bin(_from);
    _oct = oct(_from);
    _dec = str(_from);
    _hex = hex(_from);

    if (request.args.get('pad') != None):
        _bin = '0b ' + padnsplit(_bin[2:], 4);
        _oct = '0o ' + padnsplit(_oct[2:], 2);
        _dec =         padnsplit(_dec,     3);
        _hex = '0x ' + padnsplit(_hex[2:], 2);

    return Response(0, _bin, _oct, _dec, _hex).to_JSON()

if __name__ == '__main__':
    app.run()
