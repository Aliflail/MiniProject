from __future__ import unicode_literals

from django.db import models

from django.conf import settings

from django.db.models.signals import post_save
#Model for doing the test in the site we must also implement tags
class Tests(models.Model):
    test_text=models.CharField(max_length=40)
    time=models.DurationField('Duration of exam')
    times=models.DateTimeField('Date of exam')
    def __str__(self):
        return self.test_text
#Every test will have some questions
class Question(models.Model):
    question=models.CharField(max_length=256)
    testno=models.ForeignKey(Tests,on_delete=models.CASCADE)

    def __str__(self):
        return self.question
# the choices of the respective answersc.
class Choice(models.Model):
    choice=models.CharField(max_length=256)
    questions=models.ForeignKey(Question,on_delete=models.CASCADE)
    def __str__(self):
        return self.choice
class Correct(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    crctans=models.ForeignKey(Choice,on_delete=models.CASCADE)

class Testscore(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL)
    test=models.ForeignKey(Tests,on_delete=models.CASCADE)
    score=models.IntegerField(default=0)

    def _str_(self):
        return self.user.email

    def __unicode__(self):
        return self.user.email


def post_save_user_model_reciever(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Testscore.objects.create(user=instance)
        except:
            pass


post_save.connect(post_save_user_model_reciever, sender=settings.AUTH_USER_MODEL)
class compilerquestion(models.Model):
    question=models.TextField()
    code = models.TextField(blank=True)