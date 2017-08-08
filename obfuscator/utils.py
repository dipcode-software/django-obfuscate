# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib

from obfuscator.conf import settings


class ObfuscatorUtils(object):
    """ """

    @staticmethod
    def email(value, max_length, **kwargs):
        """ """
        username, domain = value.split('@')
        username = hashlib.sha224(username).hexdigest()
        length = len(username) + len(domain) + 1
        if length > max_length:
            username = username[:(max_length - length)]
        return "{username}@{domain}".format(
            username=username, domain=domain)

    @staticmethod
    def text(value, max_length=None, **kwargs):
        """ """
        hashed_value = hashlib.sha224(value).hexdigest()
        length = len(hashed_value)
        if max_length and length > max_length:
            hashed_value = hashed_value[:(max_length - length)]
        return hashed_value

    @classmethod
    def obfuscate(cls, field, value):
        name = settings.FIELDS_MAPPING.get(type(field), None)
        if not name:
            raise ValueError("No obfuscator defined for fields of type '{}'"
                             .format(type(field)))
        method = getattr(cls, name, None)
        if not method:
            raise ValueError("Obfuscator method '{}' not defined on '{}'"
                             .format(type(field), cls.__name__))
        return method(value, max_length=getattr(field, 'max_length', None),
                      unique=getattr(field, 'unique', None))


obfuscator = getattr(settings.OBFUSCATOR_CLASS, 'obfuscate')
