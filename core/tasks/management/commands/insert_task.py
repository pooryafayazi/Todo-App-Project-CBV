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
        profile = Profile.objects.get(user=2)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=2)
        profile.save()
        print(profile)
        # profiles = Profile.objects.all()
        # if profiles.exists():  # Using exists() to check if there are any profiles
        #     for profile in profiles:
        #         Task.objects.filter(complete=True, creator=profile).delete()
        # else:
        #     print("No profiles found.")
        for _ in range(15):
            complete = self.fake.boolean(chance_of_getting_true=50)
            Task.objects.create(
                creator=profile,
                title=self.fake.sentence(),
                complete=True,
                active=not complete
    )

# python manage.py insert_task