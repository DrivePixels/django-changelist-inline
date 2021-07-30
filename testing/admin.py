# -*- coding: utf-8 -*-
from urllib.parse import urlencode

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_changelist_inline import (
    ChangelistInline,
    ChangelistInlineAdmin,
    ChangelistInlineModelAdmin,
)

from testing.models import RelatedThing, Thing


@admin.register(RelatedThing)
class RelatedThingModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


class RelatedThingChangelistInline(ChangelistInline):
    model = RelatedThing

    class ChangelistModelAdmin(ChangelistInlineModelAdmin):
        list_display = ('name', 'format_actions')
        list_display_links = None
        list_per_page = 5

        def get_queryset(self, request):
            return RelatedThing.objects.filter(thing=self.parent_instance)

        @mark_safe
        def format_actions(self, obj=None):
            if obj is None:
                return self.empty_value_display

            change_link_url = reverse(
                'admin:{app_label}_{model_name}_change'.format(
                    app_label=RelatedThing._meta.app_label,
                    model_name=RelatedThing._meta.model_name,
                ),
                args=[obj.pk],
            )

            return (
                f'<a class="button" href="{change_link_url}">'
                    'Edit'  # noqa: E131
                '</a>'
            )
        format_actions.short_description = 'Actions'

        @property
        def title(self):
            return 'Linked Related Things'

        @property
        def no_results_message(self):
            return 'No Related Things?'

        def get_add_url(self, request):
            result = super().get_add_url(request)
            if result is not None:
                return result + '?' + urlencode({
                    'thing': self.parent_instance.pk,
                })

            return result

        def get_show_all_url(self, request):
            result = super().get_show_all_url(request)
            if result is not None:
                return result + '?' + urlencode({
                    'thing': self.parent_instance.pk,
                })

            return result

        def get_toolbar_links(self, request):
            return (
                '<a href="https://www.bthlabs.pl/">'
                    'BTHLabs'  # noqa: E131
                '</a>'
            )


@admin.register(Thing)
class ThingModelAdmin(ChangelistInlineAdmin):
    inlines = (RelatedThingChangelistInline,)
