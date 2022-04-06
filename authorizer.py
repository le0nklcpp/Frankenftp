# Copyright (C) 2022 le0nklcpp
# Overwrite dummy authorizer from pyftpdlib

import hashlib
import pyftpdlib.authorizers
from pyftpdlib.authorizers import DummyAuthorizer,AuthenticationFailed
# This is simple check. Setting hash algorithm means storing password hash on server, instead of password itself
def passwordonly(pwd):
 return pwd
def hashstr(s,alg):
 return alg(s.encode()).hexdigest()
def sha256hash(pwd):
 return hashstr(pwd,hashlib.sha256)
def sha512hash3(pwd):
 return hashstr(pwd,hashlib.sha3_512)
def sha256hash3(pwd):
 return hashstr(pwd,hashlib.sha3_256)
def sha384hash3(pwd):
 return hashstr(pwd,hashlib.sha3_384)
class ExtendedAuthorizer(DummyAuthorizer):
    hashmethod = passwordonly
    def __init__(self,conf):
        hashcalls={
        'none':passwordonly,
        'sha256':sha256hash,
        'sha3-512':sha512hash3,
        'sha3-256':sha256hash3,
        'sha3-384':sha384hash3
        }
        super().__init__()
        self.hashmethod = hashcalls[conf.pwhash]
    def validate_authentication(self, username, password, handler):
        msg = "Authentication failed."
        if not self.has_user(username):
            if username == 'anonymous':
                msg = "Anonymous access not allowed."
            raise AuthenticationFailed(msg)
        if username != 'anonymous':
            if self.user_table[username]['pwd'] != self.hashmethod(password):
                raise AuthenticationFailed(msg)
