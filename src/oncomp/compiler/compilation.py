import subprocess
import os
class data:
    def __init__(self,marks,output):
        self.marks=marks
        self.output=output
        print "data"+str(marks)+str(output)
    def __str__(self):
        return self.marks

class play:
    def __init__(self,prog,pname,lan,inp,outp,marks,directory):
        self.pgm=prog
        self.name=pname
        self.language=lan
        self.input=inp
        self.output=outp
        self.marks=marks
        self.directory=directory
        print input
    #runs the program well
    def run(self,pgm,out,c):
        err=self.directory+"/"+pgm+"err.txt"
        out=self.directory+"/"+out
        print pgm
        print c
        print self.directory
        command = "./oncomp/compiler/ccompile.sh %s %s %s" % (str(pgm), str(c),str(self.directory),)
        p = subprocess.call(command,shell=True)
        cor=self.output
        self.output=self.getoutput(out,err)
        if not self.evaluate(out,cor):
            self.marks=0


    def compiler(self):
        pgm=str(self.name)
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
        inp=self.directory+"/"+self.name+"inp.txt"
        g=open(inp,"w")
        g.write(self.input)
        g.close()
        out=pgm+"out"
        out=out+".txt"
        self.run(pgm,out,c)
        os.remove(inp)
        marks=self.marks
        output=self.output
        print "compiler"+str(marks)+str(output)
        result=data(marks,output)
        return result


    def getoutput(self,o,c):
        # open the error file(ie is c) to see if error exists

        if os.path.isfile(c):
            h=open(c,"r")
            r=h.read()
            h.close()
            p = r
            os.remove(c)
        # if there is no error k is false
        else:
            f=open(o,'r')
            p=f.read()
            print p
            f.close()

        return p

    def evaluate(self,a,b):
        f=open(a,"r")
        p=f.read()
        print b
        f.close()
        os.remove(a)
        if str(p).rstrip('\n') == str(b):
            return True
        else:
            return False