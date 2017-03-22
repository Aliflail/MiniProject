#!/bin/bash
# ^
crun()
{
	./a.out<$3>$1
}
jrun()
{
	java $1<$3>$2
}
prun()
{
	python $1<$3>$2 2>&1

}
cd $3
pgm=$1
out=$pgm"out.txt"
cat > $out << END_TEXT
some text here
END_TEXT
err=$pgm"err.txt"
cat > $err<< END_TEXT
END_TEXT
in=$pgm"inp.txt"
cat > $in << END_TEXT
END_TEXT

if [[ $2 = "1" ]]
then
	prog=$pgm".c"
	gcc $prog 2>$err
	crun $out $in &
	kid=$!
elif [[ $2 = "2" ]]
then
	prog=$pgm".py"
	prun $prog $out $in &
	kid=$!
elif [[ $2 = "3" ]]
then
	prog=$pgm".cpp"
	g++ $prog 2>$err
	crun $out $in &
	kid=$!
elif [[ $2 = "4" ]]			
then
	prog=$pgm".java"
	javac $prog 2>$err
	jrun $1 $out $in &
	kid=$!
else
	echo "Programming language not supported"
fi
if ! [[ -s $err ]]
then
sleep 15
kill -15 $kid
fi