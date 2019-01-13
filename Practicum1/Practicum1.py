from collections import namedtuple
INF = 1e10


reg_exp = namedtuple('reg_exp', ['prefix', 'suffix', 'whole', 'substr'],
                     defaults=[0, 0, 0, 0])


class IncorrectDataError(Exception):
    pass


def checkStackSize(stack, value):
    if len(stack) < value:
        raise IncorrectDataError("Stack underflow")


def addLetter(stack, cond):
    if cond:
        stack.append(reg_exp(1, 1, 1, 1))
    else:
        stack.append(reg_exp(0, 0, -INF, 0))


def addEmptyWord(stack):
    stack.append(reg_exp(0, 0, 0, 0))


def applyStar(stack):
    checkStackSize(stack, 1)
    cur_re = stack.pop()
    if cur_re.whole > 0:
        stack.append(reg_exp(INF, INF, INF, INF))
    else:
        cur_re = cur_re._replace(whole=max(cur_re.whole, 0))
        cur_re = cur_re._replace(substr=max(cur_re.suffix + cur_re.prefix,
                                            cur_re.substr))
        stack.append(cur_re)


def applyPlus(stack):
    checkStackSize(stack, 2)
    second_re = stack.pop()
    first_re = stack.pop()
    result_re = reg_exp()
    result_re = result_re._replace(prefix=max(first_re.prefix,
                                              second_re.prefix))
    result_re = result_re._replace(suffix=max(first_re.suffix,
                                              second_re.suffix))
    result_re = result_re._replace(whole=max(first_re.whole,
                                             second_re.whole))
    result_re = result_re._replace(substr=max(first_re.substr,
                                              second_re.substr))
    stack.append(result_re)


def applyDot(stack):
    checkStackSize(stack, 2)
    second_re = stack.pop()
    first_re = stack.pop()
    result_re = reg_exp()
    result_re = result_re._replace(prefix=max(first_re.prefix,
                                              first_re.whole +
                                              second_re.prefix))
    result_re = result_re._replace(suffix=max(first_re.suffix +
                                              second_re.whole,
                                              second_re.suffix))
    result_re = result_re._replace(whole=first_re.whole + second_re.whole)
    result_re = result_re._replace(substr=max(first_re.suffix +
                                              second_re.prefix,
                                              max(first_re.substr,
                                                  second_re.substr)))
    stack.append(result_re)


def add(stack, x, symbol):
    if symbol not in ['a', 'b', 'c', '1', '*', '.', '+']:
        IncorrectDataError("Incorrect symbol")
    if symbol.isalpha():
        addLetter(stack, (x == symbol))
    if symbol == '1':
        addEmptyWord(stack)
    if symbol == '*':
        applyStar(stack)
    if symbol == '.':
        applyDot(stack)
    if symbol == '+':
        applyPlus(stack)


def findMaxXLen(string, x):
    if len(string) == 0:
        return 0

    if x not in ['a', 'b', 'c']:
        raise IncorrectDataError("Incorrect requested symbol")
    stack = []
    for symbol in string:
        add(stack, x, symbol)

    if len(stack) > 1:
        raise IncorrectDataError("Stack overflow")

    pref, suff, whole, substr = stack.pop()
    if substr >= INF:
        return "INF"
    else:
        return substr

if __name__ == "__main__":
    string, x = input().split()
    print(findMaxXLen(string, x))
