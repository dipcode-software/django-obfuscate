# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models


_OBF_SETTINGS = getattr(settings, 'OBFUSCATOR', {})

FIELD_OBFUSCATOR_CLASS = getattr(_OBF_SETTINGS, 'FIELD_OBFUSCATOR_CLASS',
                                 'obfuscator.utils.ObfuscatorUtils')

FIELD_OBFUSCATORS = getattr(_OBF_SETTINGS, 'FIELD_OBFUSCATORS', {
    models.CharField: 'text',
    models.TextField: 'text',
    models.EmailField: 'email',
    models.IntegerField: 'int',
    models.SmallIntegerField: 'int',
    models.PositiveIntegerField: 'int',
    models.PositiveSmallIntegerField: 'int',
})

FIELDS = getattr(_OBF_SETTINGS, 'FIELDS', {})
