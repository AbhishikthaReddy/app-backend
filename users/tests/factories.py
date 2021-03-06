import factory
from django.conf import settings

from ..models import UserProfile


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username', 'email')

    username = factory.Sequence(lambda o: 'user{}'.format(o))
    email = factory.Sequence(lambda o: 'user{}@a.pl'.format(o))
    password = factory.PostGenerationMethodCall('set_password', 'default')
    profile = factory.RelatedFactory(UserProfileFactory, 'user')
