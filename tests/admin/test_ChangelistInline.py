# -*- coding: utf-8 -*-
from unittest import mock

from django.contrib import admin
from django.http import HttpRequest, QueryDict
from django.test import TestCase

from django_changelist_inline.admin import (
    ChangelistInline,
    ChangelistInlineModelAdmin,
    InlineChangeList,
)
from testing.factories import ThingFactory
from testing.models import RelatedThing, Thing


class RelatedThingChangelistInline(ChangelistInline):
    model = RelatedThing

    class ChangelistModelAdmin(ChangelistInlineModelAdmin):
        pass


class ChangelistInlineTestCase(TestCase):
    def test_init(self):
        # When
        changelist_inline = RelatedThingChangelistInline(Thing, admin.site)

        # Then
        self.assertIsNone(changelist_inline.request)
        self.assertIsNone(changelist_inline.changelist_model_admin)

    def test_bind(self):
        # Given
        fake_request = mock.Mock(spec=HttpRequest)
        fake_request.GET = QueryDict('q=test&data__has_key=test&p=2&o=-1')

        thing = ThingFactory()
        changelist_inline = RelatedThingChangelistInline(Thing, admin.site)

        with mock.patch.object(changelist_inline, 'ChangelistModelAdmin') as mock_changelist_model_admin:
            fake_changelist_model_admin = mock.Mock(
                spec=RelatedThingChangelistInline.ChangelistModelAdmin,
            )
            mock_changelist_model_admin.return_value = fake_changelist_model_admin

            # When
            changelist_inline.bind(fake_request, thing)

            # Then
            self.assertNotEqual(changelist_inline.request, fake_request)
            self.assertIsInstance(changelist_inline.request, HttpRequest)
            self.assertEqual(len(changelist_inline.request.GET), 0)
            self.assertEqual(len(changelist_inline.request.POST), 0)
            self.assertEqual(
                changelist_inline.changelist_model_admin,
                fake_changelist_model_admin,
            )

            mock_changelist_model_admin.assert_called_with(
                thing, RelatedThing, admin.site,
            )

    def test_changelist_cant_view(self):
        # Given
        fake_request = mock.Mock(spec=HttpRequest)

        thing = ThingFactory()

        changelist_inline = RelatedThingChangelistInline(Thing, admin.site)
        changelist_inline.bind(fake_request, thing)

        with mock.patch.object(changelist_inline.changelist_model_admin, 'has_view_or_change_permission') as mock_has_view_or_change_permission:  # noqa: E501
            mock_has_view_or_change_permission.return_value = False

            # Then
            self.assertIsNone(changelist_inline.changelist)

            mock_has_view_or_change_permission.assert_called_with(
                changelist_inline.request, obj=None,
            )

    def test_changelist(self):
        # Given
        fake_request = mock.Mock(spec=HttpRequest)

        thing = ThingFactory()

        changelist_inline = RelatedThingChangelistInline(Thing, admin.site)
        changelist_inline.bind(fake_request, thing)

        with mock.patch.object(changelist_inline.changelist_model_admin, 'has_view_or_change_permission') as mock_has_view_or_change_permission:  # noqa: E501
            with mock.patch.object(changelist_inline.changelist_model_admin, 'get_changelist_instance') as mock_get_changelist_instance:  # noqa: E501
                fake_changelist_instance = mock.Mock(spec=InlineChangeList)

                mock_has_view_or_change_permission.return_value = True
                mock_get_changelist_instance.return_value = fake_changelist_instance

                # Then
                self.assertEqual(
                    changelist_inline.changelist, fake_changelist_instance,
                )

                mock_get_changelist_instance.assert_called_with(
                    changelist_inline.request,
                )
