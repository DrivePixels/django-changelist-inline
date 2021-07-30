# -*- coding: utf-8 -*-
from unittest import mock

from django.contrib import admin
from django.http import HttpRequest
from django.test import TestCase

from django_changelist_inline import (
    ChangelistInline,
    ChangelistInlineAdminMixin,
    ChangelistInlineModelAdmin,
)
from testing.factories import ThingFactory, UserFactory
from testing.models import RelatedThing, Thing


class RelatedThingChangelistInline(ChangelistInline):
    model = RelatedThing

    class ChangelistModelAdmin(ChangelistInlineModelAdmin):
        pass


class ThingAdmin(ChangelistInlineAdminMixin, admin.ModelAdmin):
    inlines = [RelatedThingChangelistInline]


class ChangelistInlineAdminMixinTestCase(TestCase):
    def setUp(self):
        self.fake_user = UserFactory()

        self.fake_request = mock.Mock(spec=HttpRequest)
        self.fake_request.user = self.fake_user

        self.thing = ThingFactory()

    def test_get_inline_instances_no_obj(self):
        # Given
        thing_admin = ThingAdmin(Thing, admin.site)

        with mock.patch.object(self.fake_user, 'has_perm') as mock_has_perm:
            with mock.patch.object(RelatedThingChangelistInline, 'bind') as mock_bind:
                mock_has_perm.return_value = True

                # When
                result = thing_admin.get_inline_instances(
                    self.fake_request, obj=None,
                )

                # Then
                self.assertEqual(len(result), 0)
                self.assertFalse(mock_bind.called)

    def test_get_inline_instances(self):
        # Given
        thing_admin = ThingAdmin(Thing, admin.site)

        with mock.patch.object(self.fake_user, 'has_perm') as mock_has_perm:
            with mock.patch.object(RelatedThingChangelistInline, 'bind') as mock_bind:
                mock_has_perm.return_value = True

                # When
                result = thing_admin.get_inline_instances(
                    self.fake_request, obj=self.thing,
                )

                # Then
                self.assertEqual(len(result), 1)
                self.assertIsInstance(result[0], RelatedThingChangelistInline)

                mock_bind.assert_called_with(self.fake_request, self.thing)
