from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, Profile


class Command(BaseCommand):
    help = "Inserting dummy data into the database"
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()
        
    def handle(self, *args, **options):
        count = 0    
        while count != 5:
            user = User.objects.create_user(email=self.fake.email(), password='Pp@123456')
            profile = Profile.objects.get(user=user)
            profile.first_name = self.fake.first_name()
            profile.last_name = self.fake.last_name()
            profile.description = self.fake.paragraph(nb_sentences=2)
            profile.save()
            count += 1