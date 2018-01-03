#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from binascii import a2b_hex
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

class AESCipher(object):
    def __init__(self, key, iv=None):
        """
        :param key: aes mode
        :param key: Requires hex encoded param as a key
        :param iv: Requires hex encoded param as a iv
        """
        self.bs = 16
        self.key = a2b_hex(key)
        if iv is None:
            self.iv = Random.new().read(AES.block_size)
        else:
            self.iv = a2b_hex(iv)

    def encrypt(self, plaintext):
        """
        :param plaintext: str or bytes
        :return: bytes, aes encrypted message
        """
        if isinstance(plaintext, str):
            plaintext = bytes(plaintext, 'utf-8')
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.encrypt(self._pad(plaintext))

    def decrypt(self, ciphertext):
        """
        :param ciphertext:
        :return: bytes
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self._unpad(cipher.decrypt(ciphertext))

    def _pad(self, s):
        """
        :param s:
        :return:
        """
        return b''.join([
            s,
            (self.bs-len(s)%self.bs) * bytes([self.bs-len(s)%self.bs])
        ])

    def _unpad(self, s):
        return s[0:-(s[-1])]


def rsa_encrypt(pub_key, message):
    if isinstance(message, str):
        message = bytes(message, 'utf-8')
    # RSA/ECB/PKCS1Padding
    # 128字节一次, 兼容java平台
    ret = list()
    input_text = message[:128]
    while input_text:
        key = RSA.importKey(pub_key)
        cipher = PKCS1_v1_5.new(key)
        ret.append(cipher.encrypt(input_text))
        message = message[128:]
        input_text = message[:128]
    return b''.join(ret)