import examples
import err
import utils.utils as tools
import utils.errorHelper as error

# 存放资源

# 关键字表
keyWords = [
    'begin',
    'end',
    'if',
    'then',
    'while',
    'do',
    'const',
    'var',
    'call',
    'procedure',
    'odd'
]

# 算符与界符表
operators = [
    '+',
    '-',
    '*',
    '/',
    '=',
    '#',
    '<',
    '>',
    ':=',
    '(',
    ')',
    ',',
    '.',
    ';'
]

# 标识符表
identifiers = []

# 读入代码
code = ""

# 字符流，由code转化，方便处理
buffer = ""

# 词法分析器解析出来的单词二元组（种别，属性值）
words = []


class Word:
    def __init__(self, category='none', attribute='none'):
        self.category = category
        self.attribute = attribute

    def set(self, s: str):
        success = False

        # 关键字匹配
        for keyword in sorted(keyWords, key=lambda t: len(t), reverse=True):
            pos = s.find(keyword)
            if pos != -1:
                success = True
                self.category = keyword

                return success, len(keyword)

        # 算符匹配
        for operator in sorted(operators, key=lambda t: len(t), reverse=True):
            pos = s.find(operator)
            if pos == 0:
                success = True
                self.category = operator

                return success, len(operator)

        # 常数匹配
        if s[0].isdigit():
            pointer = 0
            while pointer < len(s) and s[pointer].isdigit():
                pointer += 1

            success = True
            self.category = 'number'
            self.attribute = int(s[:pointer])
            return success, pointer

        # 标识符匹配
        if s[0].isalpha():
            pointer = 0
            while pointer < len(s) and s[pointer].isalnum():
                pointer += 1

            if pointer > 10:
                error.showError(err.LENGTH, s[:pointer])
                return success, -1

            success = True
            self.category = 'ident'
            self.attribute = tools.findPosition(identifiers, s[:pointer])
            return success, pointer

        error.showError(err.WORD, s)

        return success, -1


if __name__ == '__main__':
    word = Word()

    # success, l = word.set(examples.exaDict['常数'].s)
    # success, l = word.set(examples.exaDict['长度>10'].s)
    success, l = word.set(examples.exaDict['非法字符'].s)
    print(success, l)
    print(word.category, word.attribute)
