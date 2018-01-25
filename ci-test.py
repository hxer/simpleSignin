#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""
import os
import unittest
from binascii import a2b_hex
from binascii import b2a_hex
from lib.clipher import AESCipher
from signin.unicomapp import UnicomApp
from signin.jd import JD, JDUser
from lib.conf import UNICOMAPP, JDong


def test_aes():
    key = 'f6b0d3f905bf02939b4f6d29f257c2ab'
    iv = '1a42eb4565be8628a807403d67dce78d'

    mobile = b'13266668888123456'
    mobile_cipher = b'33ab20e85b0453be9cf56a85bf5108b408e6fc628ae9e7f75b16cf74e886c68d'
    passwd = b'666888123456'
    passwd_cipher = b'6eae39d7dcc618fd9b6efaac88ec18da'

    aes = AESCipher(key, iv=iv)
    assert b2a_hex(aes.encrypt(mobile)) == mobile_cipher
    assert b2a_hex(aes.encrypt(passwd)) == passwd_cipher
    assert aes.decrypt(a2b_hex(mobile_cipher)) == mobile
    assert aes.decrypt(a2b_hex(passwd_cipher)) == passwd


class TestSignin(unittest.TestCase):
    def test_jd(self):
        username = os.getenv('jd_username') or JDong['username']
        password = os.getenv('jd_password') or JDong['password']
        jd =JD(username, password)
        self.assertTrue(jd.sign())


if __name__ == "__main__":
    unittest.main()
