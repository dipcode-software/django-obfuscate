# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class ObfuscateCommandTest(TestCase):

    def test_no_arguments(self):
        with self.assertRaises(CommandError):
            call_command("obfuscate")

    def test_command_with_args(self):
        call_command("obfuscate", "--model=contenttypes.contenttype",
                     "--fields=model")
        self.assertTrue(1)

    def test_command_without_args(self):
        with self.settings(OBFUSCATOR={
            'FIELDS': {
                'contenttypes.ContentType': ['model']
            }
        }):
            call_command("obfuscate")
        self.assertTrue(1)
