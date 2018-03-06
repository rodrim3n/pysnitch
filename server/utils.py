# -*- coding: utf-8 -*-

import rsa


def encrypt(data):
    return rsa.encrypt(data.encode('utf-8'))


def decrypt(data):
    return rsa.decrypt(data).decode('utf-8')
