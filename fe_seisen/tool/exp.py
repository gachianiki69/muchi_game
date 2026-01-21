CONFIG = {
    'elite': True,
    'level': 26,
    'total_exp': 2658,
    'enemy': [17, 20, 23, 26, 29, 30, 30]
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
