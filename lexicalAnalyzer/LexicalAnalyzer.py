import err
import examples
from lexicalAnalyzer import res
import utils.errorHelper as error
import utils.utils as utils


def run(code):
    res.code = code
    # 转字符流 + 预处理
    res.buffer = utils.getBuffer(res.code)

    # 识别
    for sentence in res.buffer.split(' '):
        if sentence == "":
            continue
        pointer = 0
        while pointer < len(sentence):
            newWord = res.Word()

            success, offset = newWord.set(sentence[pointer:])

            if not success:
                error.showError(err.FAIL, sentence[pointer:])
                break

            res.words.append(newWord)
            pointer += offset

    # for word in res.words:
    #     print(f'({word.category}, {word.attribute})')

    return res.words


if __name__ == '__main__':
    run(examples.exa1.s)
