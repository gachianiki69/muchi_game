CONFIG = {
    'elite': True,
    'level': 23,
    'total_exp': 2303,
#    'enemy': [13, 16, 19, 22, 25, 28, 30]
    'enemy': [18, 18, 18, 18, 18, 18, 18, 18, 18]
}

level = CONFIG['level']
total_exp = CONFIG['total_exp']

for e in CONFIG['enemy']:
    exp = (e - level) * 2 + 30

    if exp < 0:
        exp = 0

    if CONFIG['elite']:
        exp *= 2

    if exp > 100:
        exp = 100

    total_exp += exp
    level = total_exp // 100

print(total_exp)
