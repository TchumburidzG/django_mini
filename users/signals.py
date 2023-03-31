
from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

# ამ ორ რაღაცას ერთნარი ფუქციები აქვთ: თუ ახალ პროფილს შევქმნით ან დავააპდეითებთ
# (models.py-ში როა Profile მოდელი მაგაში )
# და დავწვებით შენახვას გამოიძახებს ქვემოთ მოცემულ ფუქციას.
# დეკორატორის შემთხვევაში ფუქცისს სახელი მითითებული არ გვაქ მარა ეს მე მგონი ზუსტად ფუქციის თავზე რო დგას
# მაგით ხვდება რომელი ფუქცია უნდა გამიძახოს
#post_save.connect(profileUpdated, sender=Profile))
#@receiver(post_save, sender=Profile)
def profileUpdated(sender, instance, created, **kwargs):
    print('jshdsjkhcklnskjcbkx')
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        subject = 'welcome to DevSearch'
        message = 'We are glad you are here'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()



def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

post_save.connect(profileUpdated, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)

# ზედა ორი ფუქცია და ორი ხაზი აკეთებს შემდეგ მოქმედებებს. თუ შექმნით იუზერს, დაამატებს ავტომატურად პროფილს
# ამ იუზერისთვის. თუ წავშლით იუზერს წაშლის პროფილსაც.
# თუ წავშლით პროფილს და იუზერის წაშლა დაგვავიწყდა ეს წაშლის ავტომატურად.