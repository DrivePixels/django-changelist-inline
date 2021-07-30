# -*- coding: utf-8 -*-
from unittest import mock

from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase

from django_changelist_inline.admin import (
    ChangelistInlineModelAdmin,
    InlineChangeList,
)
from testing.models import RelatedThing, Thing
from testing.factories import ThingFactory


class RelatedThingInlineModelAdmin(ChangelistInlineModelAdmin):
    pass


class InlineChangeListTestCase(TestCase):
    def setUp(self):
        self.fake_user = mock.Mock(spec=User)
        self.fake_user.has_perm.return_value = True

        self.fake_request = mock.Mock(spec=HttpRequest)
        self.fake_request.GET = {}
        self.fake_request.resolver_match = None
        self.fake_request.user = self.fake_user

        thing = ThingFactory()
        self.model_admin = RelatedThingInlineModelAdmin(
            thing, RelatedThing, admin.site,
        )

    def test_init(self):
        # When
        change_list = InlineChangeList(
            self.fake_request, Thing, ['pk'], ['pk'], [], None, None, None, 5,
            5, None, self.model_admin, None,
        )

        # Then
        self.assertIsNone(change_list.formset)
        self.assertEqual(
            change_list.add_url, '/admin/testing/relatedthing/add/',
        )
        self.assertEqual(
            change_list.show_all_url, '/admin/testing/relatedthing/',
        )
        self.assertIsNone(change_list.toolbar_links)

    def test_get_filters_params(self):
        # Give
        change_list = InlineChangeList(
            self.fake_request, Thing, ['pk'], ['pk'], [], None, None, None, 5,
            5, None, self.model_admin, None,
        )

        # When
        result = change_list.get_filters_params(params={'q': 'spam'})

        # Then
        self.assertEqual(result, {})

    def test_has_toolbar_False(self):
        # Given
        change_list = InlineChangeList(
            self.fake_request, Thing, ['pk'], ['pk'], [], None, None, None, 5,
            5, None, self.model_admin, None,
        )
        change_list.add_url = None
        change_list.show_all_url = None
        change_list.toolbar_links = None

        # Then
        self.assertFalse(change_list.has_toolbar)

    def test_has_toolbar_True_with_add_url(self):
        # Given
        change_list = InlineChangeList(
            self.fake_request, Thing, ['pk'], ['pk'], [], None, None, None, 5,
            5, None, self.model_admin, None,
        )
        change_list.add_url = 'add_url'
        change_list.show_all_url = None
        change_list.toolbar_links = None

        # Then
        self.assertTrue(change_list.has_toolbar)

    def test_has_toolbar_True_with_show_all_url(self):
        # Given
        change_list = InlineChangeList(
            self.fake_request, Thing, ['pk'], ['pk'], [], None, None, None, 5,
            5, None, self.model_admin, None,
        )
        change_list.add_url = None
        change_list.show_all_url = 'show_all_url'
        change_list.toolbar_links = None

        # Then
        self.assertTrue(change_list.has_toolbar)

    def test_has_toolbar_True_with_toolbar_links(self):
        # Given
        change_list = InlineChangeList(
            self.fake_request, Thing, ['pk'], ['pk'], [], None, None, None, 5,
            5, None, self.model_admin, None,
        )
        change_list.add_url = None
        change_list.show_all_url = None
        change_list.toolbar_links = 'toolbar_links'

        # Then
        self.assertTrue(change_list.has_toolbar)
