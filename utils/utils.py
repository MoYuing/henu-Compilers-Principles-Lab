import examples
import re


def getBuffer(code):
    """
    转字符流
    :param code:
    :return: 不存在空行、换行、注释、制表符的字符流
    """
    buffer = []
    for line in list(code.split('\n')):  # 按回车分割，line表示一行code

        if (start := line.find('//')) != -1:  # 存在单行注释
            line = line[:start]  # 只需要单行注释之前的

        line = re.sub(r'\s+', ' ', line)  # 正则替换， 将多个不可见字符替换为单个空格

        line = line.strip()  # 将行首部和尾部的多余空格删去
        line = line.strip('\t')  # 删除制表符
        if line == '':  # 无效空行
            continue

        buffer.append(' ')  # 每行间仍然用一个’ ‘ 作为分割
        buffer.extend(list(line))

    # 处理掉多行注释
    s = ''.join(buffer)
    s = re.sub(r'\(\*.*?\*\)', '', s)

    s = re.sub(r'\s+', ' ', s)

    return s


def findPosition(a: list, item):
    if item in a:
        return a.index(item)
    else:
        a.append(item)
        return len(a) - 1



if __name__ == '__main__':
    # print(getBuffer(examples.exa1.s))

    # text = "This is a (* s a m Ap le *) text with some (* words *) in parentheses."
    # clean_text = re.sub(r'\(\*.*?\*\)', '', text)
    #
    # print(clean_text)
    #
    # text = "This  is    a   sample    text       with     some     spaces."
    # clean_text = re.sub(r'\s+', ' ', text)
    #
    # print(clean_text)

    print(getBuffer(examples.exa1.s))