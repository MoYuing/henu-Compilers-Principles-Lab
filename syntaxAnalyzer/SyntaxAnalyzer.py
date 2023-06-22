import examples


class SyntaxAnalyzer:
    def __init__(self, words):
        self.tokenStream = [word.category for word in words]
        self.index = 0
        self.curToken = None
        self.errors = []

    def addError(self, expectedToken, currentToken):
        self.errors.append(f'语法错误：期待一个{expectedToken}, 但出现{currentToken}')

    def showResults(self):
        if self.errors:
            self.showErrors()
        else:
            print("语法正确")

    def showErrors(self):
        for error in self.errors:
            print(error)

    def advance(self):  # 指针移位，读入下一个word
        if self.index >= len(self.tokenStream):  # 读到末尾
            pass
        else:
            self.curToken = self.tokenStream[self.index]
        self.index += 1

    def match(self, needToken):
        if type(needToken) != type(list()):
            needToken = [needToken]

        if self.curToken in needToken:
            self.advance()
        else:
            self.addError(needToken, self.curToken)

    def program(self):
        self.advance()
        self.block()
        self.match(".")

    def block(self):
        self.constdecl()
        self.vardecl()
        self.procdecl()
        self.statement()

    def constdecl(self):
        if self.curToken == "const":
            self.match("const")
            self.constitem()

            while self.curToken == ",":
                self.match(",")
                self.constitem()

            self.match(";")

    def constitem(self):
        self.match("ident")
        self.match("=")
        self.match("number")

    def vardecl(self):
        if self.curToken == "var":
            self.match("var")
            self.match("ident")

            while self.curToken == ",":
                self.match(",")
                self.match("ident")

            self.match(";")

    def procdecl(self):
        while self.curToken == "procedure":
            self.match("procedure")
            self.match("ident")
            self.match(";")
            self.block()
            self.match(";")

    def statement(self):
        if self.curToken == "ident":
            self.assignstmt()
        elif self.curToken == "call":
            self.callstmt()
        elif self.curToken == "begin":
            self.compstmt()
        elif self.curToken == "if":
            self.ifstmt()
        elif self.curToken == "while":
            self.whilestmt()
        else:
            pass  # 因为都是可选项 不需要报错

    def assignstmt(self):
        self.match("ident")
        self.match(":=")
        self.expression()

    def callstmt(self):
        self.match("call")
        self.match("ident")

    def compstmt(self):
        self.match("begin")
        self.statement()
        while self.curToken == ";":
            self.match(";")
            self.statement()
        self.match("end")

    def ifstmt(self):
        self.match("if")
        self.condition()
        self.match("then")
        self.statement()

    def whilestmt(self):
        self.match("while")
        self.condition()
        self.match("do")
        self.statement()

    def condition(self):
        if self.curToken == "odd":
            self.match("odd")
            self.expression()
        else:
            self.expression()
            self.match(["=", "#", "<", ">"])
            self.expression()

    def expression(self):
        self.term()
        while self.curToken in ["+", "-"]:
            self.match(self.curToken)
            self.term()

    def term(self):
        self.factor()
        while self.curToken in ["*", '/']:
            self.match(self.curToken)
            self.factor()

    def factor(self):
        if self.curToken in ["+", "-"]:
            self.match(self.curToken)
        if self.curToken == "ident":
            self.match("ident")
        elif self.curToken == "number":
            self.match("number")
        elif self.curToken == "(":
            self.match("(")
            self.expression()
            self.match(")")
        else:
            self.addError('+,-,ident,number,(,)', self.curToken)


def run(code):
    analyzer = SyntaxAnalyzer(LexicalAnalyzer.run(code))
    analyzer.program()
    analyzer.showResults()


if __name__ == "__main__":
    from lexicalAnalyzer import LexicalAnalyzer

    # run(examples.exa1.s)

    # run(examples.exaDict[f'错误代码1'].s)

    # run(examples.exaDict[f'错误代码2'].s)

    # run(examples.exaDict[f'错误代码3'].s)

    run(examples.exaDict[f'错误代码4'].s)
