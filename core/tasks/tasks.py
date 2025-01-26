from celery import shared_task
from tasks.models import Task
from accounts.models import Profile

@shared_task
def deleteCompleted():
    profiles = Profile.objects.all()
    if profiles.exists():
        for profile in profiles:
            Task.objects.filter(complete=True, creator=profile).delete()
    
        
