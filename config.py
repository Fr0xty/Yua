import itertools

chars = "yua "
prefixList = list(map(''.join, itertools.product(*zip(chars.upper(), chars.lower()))))

yua_color = 16235890