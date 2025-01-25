from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, Profile
from tasks.models import Task


class Command(BaseCommand):
    help = "Inserting dummy data into the database"
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()
        
    def handle(self, *args, **options):
        user = User.objects.create_user(email=self.fake.email(), password='Pp@123456')
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=2)
        profile.save()

        for _ in range(5):
            complete = self.fake.boolean(chance_of_getting_true=50)
            Task.objects.create(
                creator=profile,
                title=self.fake.sentence(),
                complete=complete,
                active=not complete
    )
        