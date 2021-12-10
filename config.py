import itertools

chars = "yua "
prefixList = list(map(''.join, itertools.product(*zip(chars.upper(), chars.lower()))))