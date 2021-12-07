# -*- coding: utf-8 -*-
from unittest import mock

from django.contrib import admin
from django.http import HttpRequest
from django.test import TestCase

from django_changelist_inline import ChangelistInlineModelAdmin
from django_changelist_inline.admin import InlineChangeList
from testing.factories import ThingFactory
from testing.models import RelatedThing


class ChangelistInlineModelAdminTestCase(TestCase):
    def setUp(self):
        self.thing = ThingFactory()
        self.fake_request = mock.Mock(spec=HttpRequest)

    def test_init(self):
        # When
        model_admin = ChangelistInlineModelAdmin(
            self.thing, RelatedThing, admin.site,
        )

        # Then
        self.assertEqual(model_admin.parent_instance, self.thing)
        self.assertEqual(model_admin.list_editable, ())
        self.assertEqual(model_admin.list_filter, ())
        self.assertEqual(model_admin.search_fields, ())
        self.assertIsNone(model_admin.date_hierarchy)
        self.assertEqual(model_admin.sortable_by, ())

        # Account for `search_help_text` attr added in Django 4.0
        if hasattr(model_admin, 'search_help_text'):
            self.assertIsNone(model_admin.search_help_text)

    @mock.patch('django.contrib.admin.ModelAdmin.get_actions')
    def test_get_actions(self, mock_get_actions):
        # Given
        mock_get_actions.return_value = []

        model_admin = ChangelistInlineModelAdmin(
            self.thing, RelatedThing, admin.site,
        )

        # When
        result = model_admin.get_actions(self.fake_request)

        # Then
        self.assertEqual(result, [])
        self.assertFalse(mock_get_actions.called)

    def test_get_changelist(self):
        # Given
        model_admin = ChangelistInlineModelAdmin(
            self.thing, RelatedThing, admin.site,
        )

        # When
        result = model_admin.get_changelist(self.fake_request)

        # Then
        self.assertEqual(result, InlineChangeList)

    def test_title(self):
        # Given
        model_admin = ChangelistInlineModelAdmin(
            self.thing, RelatedThing, admin.site,
        )

        # Then
        self.assertEqual(
            model_admin.title, RelatedThing._meta.verbose_name_plural,
        )

    def test_no_results_message(self):
        # Given
        model_admin = ChangelistInlineModelAdmin(
            self.thing, RelatedThing, admin.site,
        )

        # Then
        self.assertEqual(
            model_admin.no_results_message,
            f'0 {RelatedThing._meta.verbose_name_plural}',
        )

    def test_get_add_url_no_add_permission(self):
        # Given
        model_admin = ChangelistInlineModelAdmin(
            self.thing, RelatedThing, admin.site,
        )

        with mock.patch.object(model_admin, 'has_add_permission') as mock_has_add_permission:
            mock_has_add_permission.return_value = False

            # Then
            self.assertIsNone(model_admin.get_add_url(self.fake_request))

            mock_has_add_permission.assert_called_with(self.fake_request)

    def test_get_add_url(self):
        # Given
        model_admin = ChangelistInlineModelAdmin(
            self.thing, RelatedThing, admin.site,
        )

        with mock.patch.object(model_admin, 'has_add_permission') as mock_has_add_permission:
            mock_has_add_permission.return_value = True

            # Then
            self.assertEqual(
                model_admin.get_add_url(self.fake_request),
                '/admin/testing/relatedthing/add/',
            )

    def test_get_show_all_url_no_view_permission(self):
        # Given
        model_admin = ChangelistInlineModelAdmin(
            self.thing, RelatedThing, admin.site,
        )

        with mock.patch.object(model_admin, 'has_view_permission') as mock_has_view_permission:
            mock_has_view_permission.return_value = False

            # Then
            self.assertIsNone(model_admin.get_show_all_url(self.fake_request))

            mock_has_view_permission.assert_called_with(
                self.fake_request, obj=None,
            )

    def test_get_show_all_url(self):
        # Given
        model_admin = ChangelistInlineModelAdmin(
            self.thing, RelatedThing, admin.site,
        )

        with mock.patch.object(model_admin, 'has_view_permission') as mock_has_view_permission:
            mock_has_view_permission.return_value = True

            # Then
            self.assertEqual(
                model_admin.get_show_all_url(self.fake_request),
                '/admin/testing/relatedthing/',
            )

    def test_get_toolbar_links(self):
        # Given
        model_admin = ChangelistInlineModelAdmin(
            self.thing, RelatedThing, admin.site,
        )

        # Then
        self.assertIsNone(model_admin.get_toolbar_links(self.fake_request))
