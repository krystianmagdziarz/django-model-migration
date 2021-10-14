from django.core.management import call_command
from django.test import TestCase
from faker import Faker

from engine.models import Subscriber, Client, User


class MigrationCommandTestCase(TestCase):
    """
        Przykładowy test jednostkowy, test należy rozszerzyć o pozostałe przypadki opisane w dokumentacji
    """
    def setUp(self):
        """
        Jeśli istnieje Client z polem email takim jak Subscriber.email i nie istnieje User
        z polem phone takim jak Client.phone i polem email różnym od Client.email
        stwórz użytkownika na podstawie modelu Client
        :return: None
        """
        fake = Faker("pl_PL")

        subscriber = Subscriber.objects.create(email=fake.email(), gdpr_consent=fake.pybool())
        self.client = Client.objects.create(email=subscriber.email, phone=fake.phone_number())

        return

    def test_migrate_data(self):
        call_command('migrate_data')

        assert User.objects.filter(email=self.client.email, phone=self.client.phone).exists()
