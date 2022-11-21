from django.core.exceptions import ObjectDoesNotExist
from task_manager.statuses.models import Statuses
from task_manager.users.models import User
from task_manager.tasks.models import Task
from django.test import TestCase
from task_manager.utils import get_fixture_data
from django.urls import reverse


class StatusesTest(TestCase):
    fixtures = ["statuses.json", "users.json"]
    test_data = get_fixture_data('test_data.json')
    user_data = get_fixture_data('users.json')
    print(test_data)

    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(
            cls.user_data[0]['fields']
        )
        cls.status = Statuses.objects.first()
        cls.status_new = Statuses.objects.create(
            **cls.test_data['statuses']['new']
        )

    def test_index_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses:index'))
        self.assertEqual(response.status_code, 200)

    def test_create_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses:create'))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('statuses:create'),
                                    self.test_data['statuses']['new'])

        self.assertRedirects(response, reverse('statuses:index'))

        status = Statuses.objects.get(name=self.status_new.name)
        self.assertEqual(status.name, self.status_new.name)

    def test_update_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses:update', args=[self.status.pk]))

        self.assertEqual(response.status_code, 200)

    def test_update(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('statuses:update', args=[self.status.pk]),
                                    self.test_data[0]['fields'])

        self.assertRedirects(response, reverse('statuses:index'))

        updated_status = Statuses.objects.get(
            name=self.status_new.name
        )
        self.assertEqual(updated_status.name, self.status_new.name)

    def test_delete_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses:delete', args=[self.status.pk]))
        request = self.client.get(reverse("statuses:delete", args=[self.status.pk]))


        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('statuses:delete', args=[self.status.pk]))

        self.assertRedirects(response, reverse('statuses:index'))

        with self.assertRaises(ObjectDoesNotExist):
            Statuses.objects.get(
                name=self.status.name
            )

    def test_bound_delete(self):
        self.client.force_login(self.user)