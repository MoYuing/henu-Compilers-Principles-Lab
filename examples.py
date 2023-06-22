class Example:
    def __init__(self, s):
        self.s = s

exaDict = {}

exa1 = Example("""
// PL/0 demo

(*
	This is a multi-line
	comment
*)

const limit=10;
var n, f, test, t1, t2;
begin
     n := 0;
     f := 1;
     while n # limit do
     begin
          n := n + 1;
          f := f * n;
     end;
     test := 1+2-3*4/(5-6)+-7;
	t1:=test*2;
	t2:=t1+test;
     call print;	// print all var
end.

""")

exaDict['例1'] = exa1

exa2 = Example("""
// PL/0 demo

(*
	This is a multi-line
	comment
*)
""")

exaDict['注释'] = exa2

exaDict['标识符'] = Example("""asdas b c asd csve asd gogogo gpTo""")

exaDict['常数'] = Example("""114514 23""")

exaDict['表达式'] = Example("""Y = 10*x + 23*abc / 2 + 1+1-2*(1+1)+(2/2) * 11""")

exaDict['长度>10'] = Example("""asddsfshvsddasdwrsasd""")

exaDict['非法字符'] = Example("""
1

^

1""")

exaDict['错误代码1'] = Example("""
// PL/0 demo

(*
	This is a multi-line
	comment
*)

const limit=10;
var n, f, test, t1, t2;
begin
     n := 0;
     f := 1;
     while n # limit do
     begin
          n := n + 1;
          f := f * n;
     end;
     test := 1+2-3*4/(5-6)+-7;
	t1:=test*2;
	t2:=t1+test;
     call print;	// print all var
end
""")

exaDict['错误代码2'] = Example("""
// PL/0 demo

(*
	This is a multi-line
	comment


const limit=10;
var n, f, test, t1, t2;
begin
     n := 0;
     f := 1;
     while n # limit do
     begin
          n := n + 1;
          f := f * n;
     end;
     test := 1+2-3*4/(5-6)+-7;
	t1:=test*2;
	t2:=t1+test;
     call print;	// print all var
end
""")

exaDict['错误代码3'] = Example("""
// PL/0 demo

(*
	This is a multi-line
	comment
*)

const limit=10;
n, f, test, t1, t2;
begin
     n := 0;
     f := 1;
     while n # limit do
     begin
          n := n + 1;
          f := f * n;
     end;
     test := 1+2-3*4/(5-6)+-7;
	t1:=test*2t2;
	t2:=t1+test;
     call print;	// print all var
end.
""")
exaDict['错误代码4'] = Example("""test := 1(()a+2-3*4/((((5-6)+-7;end.""")

if __name__ == '__main__':
    print(exa1.s)
