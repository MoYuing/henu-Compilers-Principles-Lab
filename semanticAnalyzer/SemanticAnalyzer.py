import examples
from utils.utils import findIdentName


class Node:
    def __init__(self, category, value, children=[]):
        self.category = category
        self.value = value
        self.children = children

        self.name = value


def opr(op, cnt, children=[]):
    t = op
    if op in ['+', '-', '*', '/']:
        t = 'operator'
    elif op in ['=', '<', '>', '#']:
        t = 'judge'
    elif op == ':=':
        t = 'assign'

    return Node(t, op, children)


def id(entry):
    return Node('ident', entry)


def num(value):
    return Node("value", value)


class SemanticAnalyzer:
    def __init__(self, words):
        self.tokenStream = [word for word in words]
        self.index = 0
        self.curType = None
        self.curValue = None
        self.errors = []
        self.root = None
        self.depth = {}

    def traverse(self, u: Node, cnt):
        print('|' + '--' * (cnt - 1), end=' ')
        if u.category == 'ident':
            print(f'({u.category}, {findIdentName(u.value)})')
        else:
            print(f'({u.category}, {u.value})')

        for v in u.children:
            if v:
                self.traverse(v, cnt + 1)

    def build(self):
        self.root = self.program()

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
            self.curType, self.curValue = self.tokenStream[self.index].category, self.tokenStream[self.index].attribute
            self.index += 1

    def getCurrentToken(self):
        return [self.curType, self.curValue]

    def match(self, needType):
        if type(needType) != type(list()):
            needType = [needType]

        if self.curType in needType:
            x, y = self.getCurrentToken()
            self.advance()
            return x, y
        else:
            self.addError(needType, self.curType)

    def program(self):
        self.advance()
        block = self.block()
        self.match('.')
        return block

    def block(self):
        children = [self.constdecl(), self.vardecl(), self.procdecl(), self.statement()]
        block = opr('.', 4, children)
        return block

    def constdecl(self):
        if self.curType == "const":
            self.match("const")
            tmpP = self.constitem()
            while self.curType == ",":
                self.match(",")
                constItem = self.constitem()

                tmpP = opr(',', 2, [tmpP, constItem])

            self.match(';')
            constdecl = opr('const', 1, [tmpP])
            return constdecl
        else:
            return None

    def constitem(self):
        _, entry = self.match("ident")
        tmpP = id(entry)

        self.match("=")

        _, val = self.match("number")

        constItem = opr('=', 2, [tmpP, num(val)])
        return constItem

    def vardecl(self):
        if self.curType == "var":
            self.match('var')
            _, entry = self.match('ident')
            tmpP = id(entry)

            while self.curType == ",":
                self.match(',')
                _, entry = self.match('ident')
                tmpP = opr(',', 2, [tmpP, id(entry)])

            self.match(';')

        vardecl = opr('var', 1, [tmpP])
        return vardecl

    def procdecl(self):
        tmpP = None
        while self.curType == "procedure":
            self.match('procedure')
            _, entry = self.match('ident')

            tmpPN = id(entry)

            self.match(';')
            block = self.block()

            tmpPB = block

            self.match(";")

            if tmpP is None:
                tmpP = opr('procedure', 2, [tmpPN, tmpPB])
            else:
                tmpP = opr(';', 2, [tmpP, opr('procedure', 2, [tmpPN, tmpPB])])

        return tmpP

    def statement(self):
        tmpP = None
        if self.curType == "ident":
            tmpP = self.assignstmt()
        elif self.curType == "call":
            tmpP = self.callstmt()
        elif self.curType == "begin":
            tmpP = self.compstmt()
        elif self.curType == "if":
            tmpP = self.ifstmt()
        elif self.curType == "while":
            tmpP = self.whilestmt()
        else:
            pass  # 因为都是可选项 不需要报错
        return tmpP

    def assignstmt(self):
        _, entry = self.match('ident')
        tmpP = id(entry)
        self.match(":=")
        exp = self.expression()
        assign = opr(':=', 2, [tmpP, exp])
        return assign

    def callstmt(self):
        self.match('call')
        _, entry = self.match('ident')
        call = opr('call', 1, [id(entry)])
        return call

    def compstmt(self):
        self.match('begin')
        state = self.statement()

        tmpP = state

        while self.curType == ";":
            self.match(';')
            state = self.statement()

            tmpP = opr(';', 2, [tmpP, state])

        self.match('end')
        comp = opr('begin', 1, [tmpP])
        return comp

    def ifstmt(self):
        self.match('if')
        condition = self.condition()

        tmpP = condition

        self.match('then')
        state = self.statement()

        ifs = opr('if', 2, [tmpP, state])

        return ifs

    def whilestmt(self):
        self.match("while")

        tmpP = self.condition()

        self.match("do")

        state = self.statement()
        whi = opr('while', 2, [tmpP, state])
        return whi

    def condition(self):
        if self.curType == "odd":
            self.match("odd")
            exp = self.expression()
            return opr('odd', 1, [exp])
        else:

            tmpP = self.expression()
            op, _ = self.match(["=", "#", "<", ">"])
            exp = self.expression()

            return opr(op, 2, [tmpP, exp])

    def expression(self):
        tmpP = self.term()
        while self.curType in ["+", "-"]:
            op, _ = self.match(self.curType)
            term = self.term()
            tmpP = opr(op, 2, [tmpP, term])

        return tmpP

    def term(self):
        tmpP = self.factor()
        while self.curType in ["*", '/']:
            op, _ = self.match(self.curType)
            factor = self.factor()
            tmpP = opr(op, 2, [tmpP, factor])
        return tmpP

    def factor(self):
        sign = None
        if self.curType in ["+", "-"]:
            sign = 'UPLUS' if self.curType == '+' else 'UMINUS'
            self.match(self.curType)
        tmpP = None
        if self.curType == "ident":
            _, entry = self.match("ident")
            tmpP = id(entry)
        elif self.curType == "number":
            _, v = self.match("number")
            tmpP = num(v)
        elif self.curType == "(":
            self.match("(")
            tmpP = self.expression()
            self.match(")")

        if sign:
            return opr(sign, 1, [tmpP])
        else:
            return tmpP


def run(code):
    analyzer = SemanticAnalyzer(LexicalAnalyzer.run(code))
    analyzer.build()
    analyzer.showResults()
    analyzer.traverse(analyzer.root, 1)
    analyzer.showResults()


if __name__ == "__main__":
    from lexicalAnalyzer import LexicalAnalyzer

    run(examples.exa1.s)
    # run(examples.exaDict['f5'].s)
    # run(examples.exaDict['表达式'].s)
    # run(examples.exaDict[f'错误代码1'].s)

    # run(examples.exaDict[f'错误代码2'].s)

    # run(examples.exaDict[f'错误代码3'].s)

    # run(examples.exaDict[f'错误代码4'].s)
