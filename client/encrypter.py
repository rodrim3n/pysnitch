# -*- coding: utf-8 -*-

import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES


class AESEncrypter(object):

    instance = None
    KEY = 'me dicen antorcha'

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.bs = 32
            cls.instance.key = hashlib.sha256(cls.KEY.encode()).digest()
            cls.instance.iv = Random.new().read(AES.block_size)
            cls.instance.cipher = None
        return cls.instance

    def encrypt(self, string):
        cipher = AES.new(self.instance.key, AES.MODE_OFB, self.instance.iv)
        string = self._pad(string)
        return base64.b64encode(self.iv + cipher.encrypt(string))

    def decrypt(self, enc):
        cipher = AES.new(self.instance.key, AES.MODE_OFB, self.instance.iv)
        enc = base64.b64decode(enc)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]
