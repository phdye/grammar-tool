import itertools
def combination(str1):
    result = map(''.join, itertools.product(*((c.lower(), c.upper()) for c in str1)))
    return list(result)

print(combination('usage'))
