from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from projects.tests.factories import CollaboratorFactory

from ..models import Server
from .factories import EnvironmentTypeFactory, EnvironmentResourcesFactory, ServerStatisticsFactory,\
    ServerRunStatisticsFactory, ServerFactory


class ServerTest(APITestCase):
    def setUp(self):
        collaborator = CollaboratorFactory()
        self.user = collaborator.user
        self.project = collaborator.project
        token = Token.objects.create(user=self.user)
        self.token_header = 'Token {}'.format(token.key)
        self.url_kwargs = {'namespace': self.user.username, 'project_pk': str(self.project.pk)}
        self.env_type = EnvironmentTypeFactory()
        self.env_res = EnvironmentResourcesFactory()
        self.client = self.client_class(HTTP_AUTHORIZATION=self.token_header)

    def test_create_server(self):
        url = reverse('server-list', kwargs=self.url_kwargs)
        data = dict(
            name='test',
            environment_type=str(self.env_type.pk),
            environment_resources=str(self.env_res.pk),
            project=str(self.project.pk),
            connected=[]
        )
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Server.objects.count(), 1)
        self.assertEqual(Server.objects.get().name, data['name'])

    def test_list_servers(self):
        servers_count = 4
        ServerFactory.create_batch(4, project=self.project)
        url = reverse('server-list', kwargs=self.url_kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), servers_count)

    def test_server_details(self):
        server = ServerFactory(project=self.project)
        self.url_kwargs.update({
            'pk': str(server.pk)
        })
        url = reverse('server-detail', kwargs=self.url_kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_server_update(self):
        server = ServerFactory(project=self.project)
        self.url_kwargs.update({
            'pk': str(server.pk)
        })
        url = reverse('server-detail', kwargs=self.url_kwargs)
        data = dict(
            name='test',
            environment_type=str(self.env_type.pk),
            environment_resources=str(self.env_res.pk),
            connected=[]
        )
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        db_server = Server.objects.get(pk=server.pk)
        self.assertEqual(db_server.name, data['name'])

    def test_server_partial_update(self):
        server = ServerFactory(project=self.project)
        self.url_kwargs.update({
            'pk': str(server.pk)
        })
        url = reverse('server-detail', kwargs=self.url_kwargs)
        data = dict(name='test2')
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        db_server = Server.objects.get(pk=server.pk)
        self.assertEqual(db_server.name, data['name'])

    def test_server_delete(self):
        server = ServerFactory(project=self.project)
        self.url_kwargs.update({
            'pk': str(server.pk)
        })
        url = reverse('server-detail', kwargs=self.url_kwargs)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(Server.objects.filter(pk=server.pk).first())


class ServerRunStatisticsTestCase(APITestCase):
    def setUp(self):
        collaborator = CollaboratorFactory()
        self.user = collaborator.user
        self.project = collaborator.project
        token = Token.objects.create(user=self.user)
        self.token_header = 'Token {}'.format(token.key)
        self.url_kwargs = {'namespace': self.user.username, 'project_pk': str(self.project.pk)}
        self.client = self.client_class(HTTP_AUTHORIZATION=self.token_header)

    def test_list(self):
        stats = ServerRunStatisticsFactory(server__project=self.project)
        url = reverse('serverrunstatistics-list', kwargs={
            'namespace': self.project.get_owner_name(),
            'project_pk': str(self.project.pk),
            'server_pk': str(stats.server.pk)
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            'duration': '0' + str(stats.stop - stats.start),
            'runs': 1,
            'start': stats.start.isoformat('T')[:-6] + 'Z',
            'stop': stats.stop.isoformat('T')[:-6] + 'Z',
        }
        self.assertDictEqual(response.data, expected)


class ServerStatisticsTestCase(APITestCase):
    def setUp(self):
        collaborator = CollaboratorFactory()
        self.user = collaborator.user
        self.project = collaborator.project
        token = Token.objects.create(user=self.user)
        self.token_header = 'Token {}'.format(token.key)
        self.url_kwargs = {'namespace': self.user.username, 'project_pk': str(self.project.pk)}
        self.client = self.client_class(HTTP_AUTHORIZATION=self.token_header)

    def test_list(self):
        stats = ServerStatisticsFactory(server__project=self.project)
        url = reverse('serverstatistics-list', kwargs={
            'namespace': self.project.get_owner_name(),
            'project_pk': str(self.project.pk),
            'server_pk': str(stats.server.pk)
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            'server_time': '0' + str(stats.stop - stats.start),
            'start': stats.start.isoformat('T')[:-6] + 'Z',
            'stop': stats.stop.isoformat('T')[:-6] + 'Z',
        }
        self.assertDictEqual(response.data, expected)
