import json


CONFIG = {
    'start_index': 34113,
    'first_attack': 'player',
    'player': {
        'hp': 43,
        'hit': 100,
        'def': 14,
        'atk': 27,
        'lev': 13,
        'spd': 13,
        'skl': 18,
        'skl2': 18,
        'skill': ['tsuigeki', 'renzoku', 'hissatsu'],
        'grow': {
            'mhp': 95,
            'str': 25,
            'mgc': 25,
            'skl': 40,
            'spd': 75,
            'luk': 30,
            'def': 40,
            'mdf': 15,
        },
    },
    'enemy': {
        'hp': 59,
        'hit': 0,
        'def': 17,
        'atk': 35,
        'lev': 19,
        #'spd': 19,
        'spd': 22,
        'skl': 20,
        'skill': ['ootate', ''],
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


def is_ikari(skill, current_hp, initial_hp):
    if 'ikari' not in skill:
        return False

    return current_hp <= initial_hp / 2


def is_yuusha(skill):
    return 'yuusha' in skill


def is_ootate(skill, lv):
    if 'ootate' not in skill:
        return False

    r = next_rand()

    return r < lv


def is_tokkou(skill):
    if 'tokkou' not in skill:
        return False

    _ = next_rand()

    return True


def is_resire(skill):
    return 'resire' in skill


def is_miss(hit, skill, lev):
    r = next_rand()

    if r >= hit:
        return True

    return is_ootate(skill, lev)


def player_attack():
    global player_hp, enemy_hp, enemy_hit

    hit = CONFIG['player']['hit']

    atk = CONFIG['player']['atk']
    def_ = CONFIG['enemy']['def']
    dmg = atk - def_

    if dmg <= 0:
        dmg = 1

    renzoku = False
    ryuusei = is_ryuusei(CONFIG['player']['skill'], CONFIG['player']['skl'])

    if not ryuusei:
        gekkou = is_gekkou(CONFIG['player']['skill'], CONFIG['player']['skl'])

    if not ryuusei:
        renzoku = is_renzoku(CONFIG['player']['skill'], CONFIG['player']['spd'])

    taiyou = is_taiyou(CONFIG['player']['skill'], CONFIG['player']['skl'])
    ikari = is_ikari(CONFIG['player']['skill'], player_hp, CONFIG['player']['hp'])

    if not renzoku:
        renzoku = is_yuusha(CONFIG['player']['skill'])

    if taiyou:
        ootate = is_ootate(CONFIG['enemy']['skill'], CONFIG['enemy']['lev'])

        if ootate:
            pass
        else:
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
            miss = is_miss(hit, CONFIG['enemy']['skill'], CONFIG['enemy']['lev'])

            if miss:
                continue
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
        ootate = is_ootate(CONFIG['enemy']['skill'], CONFIG['enemy']['lev'])

        if ootate:
            pass
        else:
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
        miss = is_miss(hit, CONFIG['enemy']['skill'], CONFIG['enemy']['lev'])

        if miss and not renzoku:
            return False
        elif miss and renzoku:
            pass
        else:
            if 'hissatsu' in CONFIG['player']['skill']:
                r = next_rand()

                if r < CONFIG['player']['skl2']:
                    dmg2 = atk * 2 - def_
                    enemy_hp -= dmg2
                else:
                    enemy_hp -= dmg
            elif ikari:
                _ = next_rand()

                dmg2 = atk * 2 - def_
                enemy_hp -= dmg2
            else:
                enemy_hp -= dmg

    if enemy_hp <= 0:
        return True

    if renzoku:
        miss = is_miss(hit, CONFIG['enemy']['skill'], CONFIG['enemy']['lev'])

        if miss:
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
    global player_hp, enemy_hp

    hit = enemy_hit

    atk = CONFIG['enemy']['atk']
    def_ = CONFIG['player']['def']
    dmg = atk - def_

    if dmg <= 0:
        dmg = 1

    ryuusei = False
    gekkou = False
    taiyou = False

    ryuusei = is_ryuusei(CONFIG['player']['skill'], CONFIG['player']['skl'])

    if not ryuusei:
        gekkou = is_gekkou(CONFIG['player']['skill'], CONFIG['player']['skl'])

    if not ryuusei and not gekkou:
        taiyou = is_taiyou(CONFIG['player']['skill'], CONFIG['player']['skl'])

    renzoku = is_renzoku(CONFIG['enemy']['skill'], CONFIG['enemy']['spd'])
    resire = is_resire(CONFIG['enemy']['skill'])

    if not renzoku:
        renzoku = is_yuusha(CONFIG['enemy']['skill'])

    if not resire:
        miss = is_miss(hit, CONFIG['player']['skill'], CONFIG['player']['lev'])
    else:
        r = next_rand()

        miss = r >= hit

    if miss and not renzoku:
        return False
    elif miss and renzoku:
        pass
    else:
        if is_tokkou(CONFIG['enemy']['skill']):
            dmg2 = atk * 2 - def_
            player_hp -= dmg2
        elif is_hissatsu(CONFIG['enemy']['skill'], CONFIG['enemy']['skl']):
            dmg2 = atk * 2 - def_
            player_hp -= dmg2
        else:
            player_hp -= dmg

        do_inori()
        hit = enemy_hit

        if resire:
            enemy_hp = min(enemy_hp + dmg, CONFIG['enemy']['hp'])

    if player_hp <= 0:
        return True

    if renzoku:
        miss = is_miss(hit, CONFIG['player']['skill'], CONFIG['player']['lev'])

        if miss:
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


for i in range(CONFIG['start_index'], CONFIG['start_index'] + 1000):
    rand_index = i
    battle()
