def push(stack, x):
    stack.append(x)


def pop(stack):
    return stack.pop()


def clear(stack):
    stack.clear()


def is_empty(stack):
    return len(stack) == 0


def size(stack):
    return len(stack)


def top(stack):
    return stack[len(stack)-1]


seq = "(((((((((((())))))))))))"
stack = []

def skobki228(_stack, _seq):
    for c in _seq:
        if c == "(":
            push(_stack, c)
        elif c == "{":
            push(_stack, c)
        elif c == "[":
            push(_stack, c)
        elif c == ")":
            if is_empty(_stack):
                print("nepravilno")
                return
            if top(_stack) == "(":
                pop(_stack)
            else:
                print("nepravilno")
                return
        elif c == "}":
            if is_empty(_stack):
                print("nepravilno")
                return
            if top(_stack) == "{":
                pop(_stack)
            else:
                print("nepravilno")
                return
        elif c == "]":
            if is_empty(_stack):
                print("nepravilno")
                return
            if top(_stack) == "[":
                pop(_stack)
            else:
                print("nepravilno")
                return

    if is_empty(_stack):
        print("pravilno")
    else:
        print("nepravilno")

skobki228(stack, seq)