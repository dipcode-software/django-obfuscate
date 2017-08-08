# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
from importlib import import_module

from obfuscator import conf


def import_from_string(val):
    """
    Attempt to import a class from a string representation.
    """
    try:
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '{}'. {}: {}.".format(
            val, e.__class__.__name__, e)
        raise ImportError(msg)


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

    @staticmethod
    def int(value, unique=False, **kwargs):
        """ """
        pass

    @classmethod
    def obfuscate(cls, field, value):
        name = conf.FIELD_OBFUSCATORS.get(type(field), None)
        if not name:
            raise ValueError("No obfuscator defined for fields of type '{}'"
                             .format(type(field)))
        method = getattr(cls, name, None)
        if not method:
            raise ValueError("Obfuscator method '{}' not defined on '{}'"
                             .format(type(field), cls.__name__))
        return method(value, max_length=getattr(field, 'max_length', None),
                      unique=getattr(field, 'unique', None))


obfuscator = import_from_string(conf.FIELD_OBFUSCATOR_CLASS).obfuscate
