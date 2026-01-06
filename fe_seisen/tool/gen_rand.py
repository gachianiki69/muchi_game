import copy
import json


INIT_RAND = [
    64,
    17,
    15,
    33,
    15,
    83,
    41,
    70,
    98,
    50,
    90,
    17,
    85,
    94,
    36,
    73,
    41,
    89,
    82,
    37,
    44,
    52,
    80,
    66,
    19,
    61,
    86,
    55,
    21,
    49,
    53,
    53,
    55,
    80,
    26,
    95,
    25,
    40,
    74,
    32,
    85,
    50,
    96,
    75,
    81,
    75,
    61,
    13,
    14,
    18,
    74,
    93,
    13,
    7,
    84,
]


def generate():
    r = [];
    tmp = copy.deepcopy(INIT_RAND)
    for i in range(55):
        r.append((tmp[i]+99) % 100)

    for i in range(4000):
        calc(tmp)
        for j in range(55):
            r.append((tmp[j]+99)%100)

    return r


def calc(r):
    for i in range(54, -1, -1):
        r[(i+24)%55] = (r[(i+24)%55] - r[i]) % 100

    for i in range(7):
        r[i+48] = (r[i+48] + r[i]) % 100


r = generate()

with open('rand.json', 'w') as o:
    print(json.dumps(r, indent=4), file=o)
