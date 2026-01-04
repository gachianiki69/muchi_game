CONFIG = {
    'elite': True,
    'level': 12,
    'total_exp': 1254,
    'enemy': [9, 12, 15, 18, 21, 24, 27]
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
