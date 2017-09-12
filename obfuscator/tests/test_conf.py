# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import SimpleTestCase
from mock import Mock, patch
from obfuscator.conf import import_from_string, settings


class ObfuscatorSettingsTest(SimpleTestCase):

    @patch('obfuscator.conf.import_module')
    def test_import_from_string(self, mimport_module):
        mimport_module.return_value = Mock(unittest='unittest')
        result = import_from_string('unittest.unittest')
        mimport_module.assert_called_with('unittest')
        self.assertEqual(result, 'unittest')

    @patch('obfuscator.conf.import_module')
    def test_import_from_string_import_error(self, mimport_module):
        mimport_module.side_effect = ImportError
        with self.assertRaises(ImportError):
            import_from_string('import')

    def test_getattr_not_defined(self):
        with self.assertRaises(AttributeError):
            settings.__getattr__('DUMMY')

    def test_getattr_default(self):
        self.assertEqual(settings.FIELDS, {})

    def test_getattr_user(self):
        with self.settings(OBFUSCATOR={'FIELDS': 'unit'}):
            self.assertEqual(settings.FIELDS, 'unit')

    @patch('obfuscator.conf.import_from_string')
    def test_getattr_import_string(self, mimport_from_string):
        mimport_from_string.return_value = 'unittest'
        result = settings.OBFUSCATOR_CLASS
        mimport_from_string.assert_called_with(
            'obfuscator.utils.ObfuscatorUtils')
        self.assertEqual(result, 'unittest')
