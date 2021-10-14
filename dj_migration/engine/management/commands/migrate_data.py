from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.forms.models import model_to_dict
from engine.models import (
    Subscriber,
    SubscriberSMS,
    Client,
    User
)


class Command(BaseCommand):
    help = 'Migrate data from one model to another'

    def handle(self, *args, **options):
        self.handle_migrations(Subscriber, 'email', ('phone', 'email'))
        self.handle_migrations(SubscriberSMS, 'phone', ('email', 'phone'))

    def handle_migrations(self, from_model,
                          from_param: str = 'email',
                          client_params: tuple = ('phone', 'email')):

        subscribers = from_model.objects.exclude(**{f"{from_param}__in": User.objects.all().values(from_param)})

        for subscriber in subscribers:
            client = Client.objects.filter(**{f"{from_param}": getattr(subscriber, from_param)})

            if client.exists():
                """
                    Jeśli istnieje Client z polem {from_param} takim jak {from_model}.{from_param} i istnieje User 
                    z polem client_params[0] takim jak Client.client_params[0] i polem client_params[1] różnym 
                    od Client.client_params[1] zapisz id i {from_param} subskrybenta do pliku {from_model}_conflicts.csv
                """
                user_conflict = client.filter(
                    Q(**{f"{client_params[0]}__in": User.objects.all().values(client_params[0])})
                    & ~Q(**{f"{client_params[1]}__in": User.objects.all().values(client_params[1])})
                )
                if user_conflict.exists():
                    f = open(f'{from_model._meta.verbose_name}_conflicts.csv', 'w+')
                    f.write(f'{subscriber.pk}:{getattr(subscriber, from_param)}')
                    f.close()
                    self.stdout.write(self.style.WARNING(f'Detected subscriber "{subscriber.pk}" conflict.'))
                else:
                    """
                        Jeśli istnieje Client z polem {from_param} takim jak {from_model}.{from_param} i nie istnieje 
                        User z polem client_params[0] takim jak Client.client_params[0] i polem client_params[1] 
                        różnym od Client.client_params[1] stwórz użytkownika na podstawie modelu Client
                    """
                    try:
                        User.objects.create(
                            gdpr_consent=subscriber.gdpr_consent,
                            **model_to_dict(client.first(), fields=["email", "phone"])
                        )
                        self.stdout.write(self.style.SUCCESS(f'Successfully migrated subscriber "{subscriber.pk}"'))
                    except ValidationError:
                        f = open('phone_conflicts.csv', 'w+')
                        f.write(f'{client.first().pk}:{client.first().email}:{client.first().phone}')
                        f.close()
            else:
                """
                    Jeśli nie istnieje Client z polem {from_param} takim jak {from_model}.{from_param}, 
                    stwórz użytkownika z pustym polem client_params[0]
                """
                User.objects.create(**{f"{from_param}": getattr(subscriber, from_param)}, **{f"{client_params[0]}": ""})
                self.stdout.write(
                    self.style.SUCCESS(f'Created user from {from_model._meta.verbose_name} "{subscriber.pk}" with blank {client_params[0]}'))
