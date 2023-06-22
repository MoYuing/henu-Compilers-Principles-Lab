import err


def showError(t, massage='??'):
    print("!!  ", end="")
    if t == err.WORD:  # 非法字符
        print(f'在{massage if len(massage) <= 10 else massage[:10] + "..."} 中出现非法字符 ')
    elif t == err.LENGTH:
        print('标识符长度>10:{}'.format(massage))
    elif t == err.FAIL:
        print('匹配失败， 当前未解析代码传为{}'.format(massage if len(massage) <= 10 else massage[:10] + "..."))
    else:
        pass

