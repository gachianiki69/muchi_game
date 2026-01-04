from game.fe.seisen import rand


def level_up(grow):
    lvup = []
    PARAM_TABLE = [
        {
            'key': 'mhp',
            'label': ['MHP', 'MHP2']
        },
        {
            'key': 'str',
            'label': ['STR', 'STR2']
        },
        {
            'key': 'mgc',
            'label': ['MGC', 'MGC2']
        },
        {
            'key': 'skl',
            'label': ['SKL', 'SKL2']
        },
        {
            'key': 'spd',
            'label': ['SPD', 'SPD2']
        },
        {
            'key': 'luk',
            'label': ['LUK', 'LUK2']
        },
        {
            'key': 'def',
            'label': ['DEF', 'DEF2']
        },
        {
            'key': 'mdf',
            'label': ['MDF', 'MDF2']
        },
    ]

    for i in PARAM_TABLE:
        r = rand.next()

        if r < grow[i['key']] - 100:
            lvup.append(i['label'][1])
        elif r < grow[i['key']]:
            lvup.append(i['label'][0])

    return lvup
