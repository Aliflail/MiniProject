from subprocess import call
from django.conf import settings
import os
from oncomp.models import canswer
class data:
    def __init__(self,marks,output):
        self.marks=marks
        self.output=output
    def __str__(self):
        return self.marks

class play:
    def __init__(self,prog,pname,lan,inp,outp,marks,directory):
        print prog,pname,lan,inp,outp,marks,directory
        self.pgm=prog
        self.name=pname
        self.language=lan
        self.input=inp
        self.output=outp
        self.marks=marks
        self.directory=directory
    def run(self,pgm,out,c):
        err=self.directory+"/"+pgm+"err.txt"
        cor=self.directory+"/"+pgm+"cor.txt"
        out=self.directory+"/"+out

        call("./ccompile.sh %s %s %s" %(pgm,str(c),self.directory),shell=True)
        self.output=self.getoutput(out,err)
        if not self.evaluate(out,cor):
            self.marks=0
        os.remove(out)
        os.remove(pgm)

    def compiler(self):
        pgm=self.name
        lc=self.language
        if lc=='c_pp':
            c=1
        elif lc=='python':
            c=2
        elif lc=='c_cpp':
            c=3
        elif lc=='java':
            c=4
        prog=self.pgm
        fname=pgm
        if c==1:
            fname=fname+".c"
        elif c==2:
            fname=fname+".py"
        elif c==3:
            fname=fname+".cpp"
        elif c==4:
            fname=fname+".java"
        fname=self.directory+"/"+fname
        f=open(fname,"w")
        f.write(prog)
        f.close()
        out=pgm+"out"
        out=out+".txt"
        self.run(pgm,out,c)
        result=data(self.marks,self.output)
        print result
        return result

    def getoutput(o,c):
        h=open(c,"r")
        r=h.read()
        h.close()
        if os.stat(c).st_size == 0:
            k=False
        else:
            k=True
        if k:
            f=open(o,"r")
            p=f.read()
            f.close()
        else:
            p=r
        os.remove(c)
        return p
    def evaluate(a,b):
        f=open(a,"r")
        p=f.read()
        f.close()
        g=open(b,"r")
        q=g.read()
        g.close()
        os.remove(b)
        if p==q:
            return True
        else:
            return False