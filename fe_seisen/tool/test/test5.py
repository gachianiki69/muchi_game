import json


CONFIG = {
    'start_index': 15950,
    'first_attack': 'player',
    'player': {
        'hp': 46,
        'hit': 100,
        'def': 15,
        'atk': 31,
        'lev': 18,
        'spd': 20,
        'skl': 23,
        'skl2': 49,
        'skill': ['tsuigeki', 'gekkou'],
        'grow': {
            'mhp': 110,
            'str': 30,
            'mgc': 5,
            'skl': 80,
            'spd': 30,
            'luk': 20,
            'def': 30,
            'mdf': 5,
        },
    },
    'enemy': {
        'hp': 66,
        'hit': 29,
        'def': 18,
        'atk': 36,
        'lev': 27,
        'spd': 0,
        'skill': ['yuusha'],
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

    start_rand = rand_index
    player_hp = CONFIG['player']['hp']
    enemy_hp = CONFIG['enemy']['hp']
    enemy_hit = CONFIG['enemy']['hit']
    inori = False

    if CONFIG['first_attack'] != 'enemy':
        while True:
            r = player_attack()

            if r:
                break

            r = enemy_attack()

            if r:
                break

            if 'tsuigeki' in CONFIG['player']['skill']:
                r = player_attack()

                if r:
                    break
    else:
        while True:
            r = enemy_attack()

            if r:
                break

            r = player_attack()

            if r:
                break

            if 'tsuigeki' in CONFIG['enemy']['skill']:
                r = enemy_attack()

                if r:
                    break

    if player_hp > 0:
        lvup = level_up()
        print(f'{start_rand}: {lvup}', file=f)
    else:
        print(f'{start_rand}: LOSE', file=f)


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


def is_taiyou(skill, skl):
    if 'taiyou' not in skill:
        return False

    r = next_rand()

    return r < skl


def is_ryuusei(skill, skl):
    if 'ryuusei' not in skill:
        return False

    r = next_rand()

    return r < skl


def is_gekkou(skill, skl):
    if 'gekkou' not in skill:
        return False

    r = next_rand()

    return r < skl


def is_yuusha(skill):
    return 'yuusha' in skill


def player_attack():
    global player_hp, enemy_hp, enemy_hit

    hit = CONFIG['player']['hit']

    atk = CONFIG['player']['atk']
    def_ = CONFIG['enemy']['def']
    dmg = atk - def_

    if dmg <= 0:
        dmg = 1

    renzoku = is_renzoku(CONFIG['player']['skill'], CONFIG['player']['spd'])
    ryuusei = is_ryuusei(CONFIG['player']['skill'], CONFIG['player']['skl'])
    gekkou = is_gekkou(CONFIG['player']['skill'], CONFIG['player']['skl'])
    taiyou = is_taiyou(CONFIG['player']['skill'], CONFIG['player']['skl'])

    if not renzoku:
        renzoku = is_yuusha(CONFIG['player']['skill'])

    if taiyou:
        if 'hissatsu' in CONFIG['player']['skill']:
            r = next_rand()

            if r < CONFIG['player']['skl2']:
                dmg2 = atk * 2 - def_
                enemy_hp -= dmg2
                player_hp += dmg
            else:
                enemy_hp -= dmg
                player_hp += dmg
        else:
            enemy_hp -= dmg
            player_hp += dmg

        if player_hp > CONFIG['player']['hp']:
            player_hp = CONFIG['player']['hp']

        global inori

        inori = False
        enemy_hit = CONFIG['enemy']['hit']
        do_inori()
    elif ryuusei:
        for i in range(5):
            r = next_rand()

            if r >= hit and not renzoku:
                continue
            elif r >= hit and renzoku:
                pass
            else:
                if 'hissatsu' in CONFIG['player']['skill']:
                    r = next_rand()

                    if r < CONFIG['player']['skl2']:
                        dmg2 = atk * 2 - def_
                        enemy_hp -= dmg2
                    else:
                        enemy_hp -= dmg
                else:
                    enemy_hp -= dmg

            if enemy_hp <=0:
                break
    elif gekkou:
        if 'hissatsu' in CONFIG['player']['skill']:
            r = next_rand()

            if r < CONFIG['player']['skl2']:
                dmg2 = atk * 2
                enemy_hp -= dmg2
            else:
                enemy_hp -= atk
        else:
            enemy_hp -= atk
    else:
        r = next_rand()

        if r >= hit and not renzoku:
            return False
        elif r >= hit and renzoku:
            pass
        else:
            if 'hissatsu' in CONFIG['player']['skill']:
                r = next_rand()

                if r < CONFIG['player']['skl2']:
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

                if r < CONFIG['player']['skl2']:
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

    if 'taiyou' in CONFIG['player']['skill']:
        _ = next_rand()
    elif 'ryuusei' in CONFIG['player']['skill']:
        _ = next_rand()
    elif 'gekkou' in CONFIG['player']['skill']:
        _ = next_rand()

    renzoku = is_yuusha(CONFIG['enemy']['skill'])

    r = next_rand()

    if r >= hit and not renzoku:
        return False
    elif r >= hit and renzoku:
        pass
    else:
        player_hp -= dmg
        do_inori()

    if renzoku:
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

    if r < CONFIG['player']['grow']['mhp'] - 100:
        lvup.append('MHP2')
    elif r < CONFIG['player']['grow']['mhp']:
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


for i in range(CONFIG['start_index'], CONFIG['start_index'] + 100):
    rand_index = i
    battle()
