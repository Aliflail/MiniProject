from __future__ import unicode_literals
from tests import models as tmodels
from django.db import models
from django.conf import settings
# Create your models here.
class Compilerquestion(models.Model):
    prog = models.TextField(default="")
    pname = models.CharField(max_length=256)
    mark = models.IntegerField(default=0)
    test_id =models.ForeignKey(tmodels.Apt_Test,on_delete=models.CASCADE)
    time=models.DurationField(default="0:30:00")

    def __str__(self):
        return self.prog

class CompilerTestcases(models.Model):
    testcases=models.CharField(max_length=500)
    test_out = models.TextField(max_length=1000, default='No Output')
    question_id = models.ForeignKey(Compilerquestion, on_delete=models.CASCADE)

    def __str__(self):
        return self.test_out


class canswer(models.Model):
    uid=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    tid=models.ForeignKey(tmodels.Apt_Test,on_delete=models.CASCADE)
    qid = models.ForeignKey(Compilerquestion,on_delete=models.CASCADE)
    out=models.TextField(default="")
    program=models.TextField(default="")
    language=models.IntegerField(default=0)
    class Meta:
        db_table="answer"

    def __str__(self):
        return self.prog
