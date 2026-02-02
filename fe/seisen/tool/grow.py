import json

from game.fe.seisen import level, rand


with open('grow.json') as f:
    config = json.load(f)

for i in range(config['start_index'], config['start_index'] + 50000):
    prev = []

    for j in range(i - 6, i):
        prev.append(str(rand.get(j)).zfill(2))

    rand.set_index(i)
    lvup = level.level_up(config['grow'])
    print(f'{i}: {prev}: {lvup}')
