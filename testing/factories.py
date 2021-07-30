# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
import factory

from testing.models import RelatedThing, Thing


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.Faker('ascii_email')
    username = factory.Faker('ascii_email')
    password = factory.Faker('password')
    is_staff = False


class ThingFactory(factory.Factory):
    class Meta:
        model = Thing

    name = factory.Faker('words', nb=1)
    data = factory.LazyAttribute(lambda thing: {'thing': True})


class RelatedThingFactory(factory.Factory):
    class Meta:
        model = RelatedThing

    name = factory.Faker('words', nb=1)
    data = factory.LazyAttribute(lambda thing: {'related_thing': True})
