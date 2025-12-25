import json


CONFIG = {
    'player': {
        'hp': 31,
        'hit': 46,
        'def': 9,
        'atk': 22,
        'lev': 7,
        'grow': {
            'mhp': 60,
            'str': 50,
            'mgc': 5,
            'skl': 10,
            'spd': 20,
            'luk': 40,
            'def': 20,
            'mdf': 10,
        },
    },
    'enemy': {
        'hp': 63,
        'hit': 39,
        'def': 13,
        'atk': 34,
        'lev': 23,
    }
}

player_hp = 0
enemy_hp = 0
enemy_hit = 0
inori = False


RAND = None
rand_index = 8119

f = open('log.txt', 'w')


with open('rand.json') as o:
    RAND = json.load(o)


def battle():
    global player_hp, enemy_hp, enemy_hit, inori

    player_hp = CONFIG['player']['hp']
    enemy_hp = CONFIG['enemy']['hp']
    enemy_hit = CONFIG['enemy']['hit']
    inori = False

    while True:
        r = player_attack()

        if r:
            break

        r = enemy_attack()

        if r:
            break

    if player_hp > 0:
        lvup = level_up()
        print(lvup, file=f)
    else:
        print('LOSE', file=f)



def player_attack():
    global enemy_hp

    hit = CONFIG['player']['hit']

    atk = CONFIG['player']['atk']
    def_ = CONFIG['enemy']['def']
    dmg = atk - def_

    if dmg <= 0:
        dmg = 1

    r = next_rand()

    if r >= hit:
        return False

    enemy_hp -= dmg

    return enemy_hp <= 0


def enemy_attack():
    global player_hp

    hit = enemy_hit

    atk = CONFIG['enemy']['atk']
    def_ = CONFIG['player']['def']
    dmg = atk - def_

    if dmg <= 0:
        dmg = 1

    r = next_rand()

    if r >= hit:
        return False

    player_hp -= dmg
    do_inori()

    return player_hp <= 0


def do_inori():
    global enemy_hit, inori

    if inori:
        return

    hp = player_hp

    if hp >= 10:
        return

    enemy_hit -= (10 - hp) * 10
    inori = True


def level_up():
    lvup = []

    lvup.append(rand_index)

    r = next_rand()

    if r < CONFIG['player']['grow']['mhp']:
        lvup.append('MHP')

    r = next_rand()

    if r < CONFIG['player']['grow']['str']:
        lvup.append('STR')

    r = next_rand()

    if r < CONFIG['player']['grow']['mgc']:
        lvup.append('MGC')

    r = next_rand()

    if r < CONFIG['player']['grow']['skl']:
        lvup.append('SKL')

    r = next_rand()

    if r < CONFIG['player']['grow']['spd']:
        lvup.append('SPD')

    r = next_rand()

    if r < CONFIG['player']['grow']['luk']:
        lvup.append('LUK')

    r = next_rand()

    if r < CONFIG['player']['grow']['def']:
        lvup.append('DEF')

    r = next_rand()

    if r < CONFIG['player']['grow']['mdf']:
        lvup.append('MDF')

    return lvup


def next_rand():
    global rand_index

    r = RAND[rand_index]
    rand_index += 1

    return r


for i in range(8234, 8334):
    rand_index = i
    battle()
