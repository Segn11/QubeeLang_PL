# Auto-generated from .yl (Afaan Oromoo language)
def faktooriyal(n):
    i = 1
    res = 1
    while (i < (n + 1)):
        res = (res * i)
        i = (i + 1)
    return res
num = 6
ans = faktooriyal(num)
print('Faktooriyal', num, '=', ans)
