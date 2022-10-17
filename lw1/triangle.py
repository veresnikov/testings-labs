import sys

MAX = 2.76392450374688E+040
MIN = -MAX


def check_overflow(num: float):
    if num > MAX or num < MIN:
        raise OverflowError


if len(sys.argv) != 4:
    print('неизвестная ошибка')
    exit()

a = 0
b = 0
c = 0

try:
    a = float(sys.argv[1])
    b = float(sys.argv[2])
    c = float(sys.argv[3])

    check_overflow(a)
    check_overflow(b)
    check_overflow(c)
except ValueError:
    print('неизвестная ошибка')
    exit()
except OverflowError:
    print('неизвестная ошибка')
    exit()


def eqWithOverflowProtect(left: float, right: float) -> bool:
    return left - right < sys.float_info.min


def eq(left: float, right: float) -> bool:
    return abs(left - right) < sys.float_info.min


if eqWithOverflowProtect(a, 0) or eqWithOverflowProtect(b, 0) or eqWithOverflowProtect(c, 0) or eqWithOverflowProtect(
        a + b, c) or eqWithOverflowProtect(b + c, a) or eqWithOverflowProtect(c + a, b):
    print('не треугольник')
    exit()

if eq(a, b) and eq(b, c):
    print('равносторонний')
elif eq(a, b) or eq(a, c) or eq(b, c):
    print('равнобедренный')
else:
    print('обычный')
