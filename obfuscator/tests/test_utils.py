# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.test import SimpleTestCase
from obfuscator.utils import ObfuscatorUtils


class ObfuscatorUtilsTest(SimpleTestCase):

    def test_email(self):
        self.assertEqual(
            ObfuscatorUtils.email('unit@test.dev', 100),
            '5a40179cd576e515814524d9393c6601da6335b2d426e8ef20370ae3@test.dev'
        )

    def test_email_max_length(self):
        self.assertEqual(
            ObfuscatorUtils.email('unit@test.dev', 10), '5@test.dev')

    def test_text(self):
        self.assertEqual(
            ObfuscatorUtils.text('unittest'),
            '26a824a52b35848551eb7fc48f552635170b52f9857f9f8cddcc0ae2')

    def test_text_max_length(self):
        self.assertEqual(ObfuscatorUtils.text('unittest', 5), '26a82')

    def test_obfuscate_field_error(self):
        with self.assertRaises(ValueError):
            ObfuscatorUtils.obfuscate('field', None)

    def test_obfuscate_method(self):
        with self.settings(
                OBFUSCATOR={'FIELDS_MAPPING': {models.IntegerField: 'int'}}):
            with self.assertRaises(ValueError):
                ObfuscatorUtils.obfuscate(models.IntegerField(), 'unittest')

    def test_obfuscate_return(self):
        self.assertEqual(
            ObfuscatorUtils.obfuscate(models.TextField(), 'unittest'),
            '26a824a52b35848551eb7fc48f552635170b52f9857f9f8cddcc0ae2')
