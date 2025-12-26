import json


CONFIG = {
    'player': {
        'hp': 21,
        'hit': 56,
        'def': 1,
        'atk': 13,
        'lev': 3,
        'spd': 13,
        'skl': 4,
        'skill': ['inori', 'renzoku'],
        'grow': {
            'mhp': 50,
            'str': 10,
            'mgc': 30,
            'skl': 10,
            'spd': 10,
            'luk': 30,
            'def': 10,
            'mdf': 40,
        },
    },
    'enemy': {
        'hp': 44,
        'hit': 55,
        'def': 9,
        'atk': 21,
        'lev': 14,
    }
}

player_hp = 0
enemy_hp = 0
enemy_hit = 0
inori = False


RAND = None
rand_index = 0

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


def is_renzoku(skill, spd):
    if 'renzoku' not in skill:
        return False

    r = next_rand()

    return r < spd + 20


def is_hissatsu(skill, skl):
    if 'hissatsu' not in skill:
        return False

    r = next_rand()

    return r < skl


def player_attack():
    global enemy_hp

    hit = CONFIG['player']['hit']

    atk = CONFIG['player']['atk']
    def_ = CONFIG['enemy']['def']
    dmg = atk - def_

    if dmg <= 0:
        dmg = 1

    renzoku = is_renzoku(CONFIG['player']['skill'], CONFIG['player']['spd'])

    r = next_rand()

    if r >= hit and not renzoku:
        return False
    elif r >= hit and renzoku:
        pass
    else:
        if 'hissatsu' in CONFIG['player']['skill']:
            r = next_rand()

            if r < CONFIG['player']['skl']:
                dmg2 = atk * 2 - def_
                enemy_hp -= dmg2
            else:
                enemy_hp -= dmg
        else:
            enemy_hp -= dmg

    if enemy_hp <= 0:
        return True

    if renzoku:
        r = next_rand()

        if r >= hit:
            return False
        else:
            if 'hissatsu' in CONFIG['player']['skill']:
                r = next_rand()

                if r < CONFIG['player']['skl']:
                    dmg2 = atk * 2 - def_
                    enemy_hp -= dmg2
                else:
                    enemy_hp -= dmg
            else:
                enemy_hp -= dmg

            if enemy_hp <= 0:
                return True

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

    if 'inori' not in CONFIG['player']['skill']:
        return

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


for i in range(9464, 9564):
    rand_index = i
    battle()
