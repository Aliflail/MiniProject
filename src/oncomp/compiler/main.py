from .compilation import play
from .compilation import data
import os
from oncomp.models import CompilerTestcases
class process:
    #creates a process class instance
    def __init__(self,prog,pname,lan,marks,qid,uid):
        self.pgm=prog
        self.name=pname
        self.language=lan
        self.marks=marks
        self.qid=qid
        self.uid=uid
        print self.pgm,self.name,self.language,self.marks,self.qid,self.uid
    #i think core returns the mark calculated as output
    def core(self):
        a=CompilerTestcases.objects.filter(question_id=self.qid)
        n=a.count()
        directory=self.start()
        d=0
        if n!=0:
            d=(self.marks)/n

        mark=0
        flag=False
        fin=0
        for i in a:
            o=play(self.pgm,self.name,self.language,i.testcases,i.test_out,d,directory)

            dat=o.compiler()

            mar=dat.marks
            mark=mark+mar
            if flag==False:
                fin=dat.output
                print "core"+fin
                flag=True
        final=data(mark,fin)
        return final
    def start(self):
        cur=os.getcwd()
        directory=cur+"/oncomp/compiler/"+str(self.uid)
        print directory
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory