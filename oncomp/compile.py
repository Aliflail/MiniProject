from subprocess import call
print "\nstart\n"
pgm="prog"
c=input("Select : ")
if(c is 1):
	pgm+=".c"
	call("./ccompile.sh %s %s" %(pgm,str(c)),shell=True)
elif(c is 2):
	pgm+=".py"
	call("./ccompile.sh %s %s" %(pgm,str(c)),shell=True)
elif(c is 3):
	pgm+=".cpp"
	call("./ccompile.sh %s %s" %(pgm,str(c)),shell=True)
elif(c is 4):
	pgm+=".java"
	call("./ccompile.sh %s %s" %(pgm,str(c)),shell=True)
else:
        print "\nLanguage not supported"
print "\nend"
