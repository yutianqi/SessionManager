#!/usr/bin/env python3
# encoding=utf8

import base64

class Base64Utils():

    @classmethod
    def encode(cls, plaintext):
        return base64.b64encode(plaintext.encode('utf-8')).decode('utf-8')

    @classmethod
    def decode(cls, encodedtext):
        return base64.b64decode(encodedtext.encode("utf-8")).decode("utf-8")
        
