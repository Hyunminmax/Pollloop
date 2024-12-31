from random import randint
from uuid import uuid4

from faker import Faker
from django.core.management.base import BaseCommand
from django_seed import Seed
from user.models import CustomUser

class Command(BaseCommand):
    help = "Seed users"

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            help='몇명의 유저 데이터를 만들지',
        )

    def handle(self, *args, **options):
        count = options.get('count')
        seeder = Seed.seeder()

        seeder.add_entity(
            CustomUser,
            count,
            {
                "email"         : lambda  n: seeder.faker.email(),
                "name"          : lambda n: Faker("ko_KR").name(),
                "profile"       : lambda n: seeder.faker.uri(),
                "age"           : lambda n: seeder.faker.random_int(1, 100),
                "refresh_token" : lambda n: seeder.faker.sha256(),
                "uuid"          : lambda n: uuid4(),
                "password"      : lambda n: seeder.faker.password(),
                "is_superuser"  : False,
            },
        )
        seeder.execute()