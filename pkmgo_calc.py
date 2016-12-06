import csv, json, argparse, pprint

#not safe here, should add exception handling later
with open('PKMBase.csv') as cf:
    r = csv.reader(cf, delimiter=',')
    base_stat = [dict(zip(['num','name','hp','atk','def'], row)) for row in r]
    for stat in base_stat:
        stat['num'] = int(stat['num'])
        stat['atk'] = int(stat['atk'])
        stat['def'] = int(stat['def'])
        stat['hp'] = int(stat['hp'])
    
#prepend a dummy element to match index with pokedex number
base_stat.insert(0, [])

#starting from level 1, index = level*2 - 2
sd_cost = [0, 200, 400, 600, 800, 1200, 1600, 2000, 2400, 3000, 3600, 4200, 
4800, 5600, 6400, 7200, 8000, 9000, 10000, 11000, 12000, 13300, 
14600, 15900, 17200, 18800, 20400, 22000, 23600, 25500, 27400, 29300, 
31200, 33400, 35600, 37800, 40000, 42500, 45000, 47500, 50000, 53000, 
56000, 59000, 62000, 65500, 69000, 72500, 76000, 80000, 84000, 88000, 
92000, 96500, 101000, 105500, 110000, 115000, 120000, 125000, 130000, 
136000, 142000, 148000, 154000, 161000, 168000, 175000, 182000, 
190000, 198000, 206000, 214000, 223000, 232000, 241000, 250000]

candy_cost = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 
54, 56, 58, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 94, 98, 102, 
106, 110, 114, 118, 122, 126, 130, 136, 142, 148, 154, 162, 170, 178, 
186, 196, 206, 216, 226, 238, 250, 262, 274]

cp_mul = [0.094,0.135137,0.166398,0.192651,0.215732,0.236573,0.25572,
           0.27353,0.29025,0.306057,0.321088,0.335445,0.349213,0.362458,
           0.375236,0.387592,0.399567,0.411194,0.4225,0.432926,0.443108,
           0.45306,0.462798,0.472336,0.481685,0.490856,0.499858,0.508702,
           0.517394,0.525943,0.534354,0.542636,0.550793,0.558831,0.566755,
           0.574569,0.582279,0.589888,0.5974,0.604819,0.612157,0.619399,0.626567,
           0.633645,0.640653,0.647576,0.654436,0.661215,0.667934,0.674578,0.681165,
           0.687681,0.694144,0.700539,0.706884,0.713165,0.719399,0.725572,0.7317,
           0.734741,0.737769,0.740786,0.743789,0.746781,0.749761,0.752729,0.755686,
           0.75863,0.761564,0.764486,0.767397,0.770297,0.773187,0.776065,0.778933,
           0.78179,0.784637,0.787474,0.7903]

class Pokemon:
    cp = None
    total_stardust_cost = None
    total_candy_cost = None
    #create an exact pokemon with all parameters
    def __init__(self, num, a, d, h, level, num_upgrades = None, catch_date = None, 
                move1_num = None, move1_name = None, move2_num = None, move2_name = None,
                height = None, weight = None, nickname = None):
        if num < 1 or num > 151:
            raise ValueError('No pokemon found with #{}'.format(num))
        if a < 0 or a > 15 or d < 0 or d > 15 or h < 0 or h > 15:
            raise ValueError('Pokemon iv is out of bound')
        if (isinstance(level,float) and not (level*2).is_integer()) or level < 1 or level > 39:
            raise ValueError('Pokemon level: {} is not valid'.format(level))
        self.num = num
        self.a = a
        self.d = d
        self.h = h
        self.level = level
        self.level_idx = int(level*2 - 2)
        self.num_upgrades = num_upgrades
        self.catch_date = catch_date
        self.move1_num = move1_num
        self.move1_name = move1_name
        self.move2_num = move2_num
        self.move2_name = move2_name
        self.height = height
        self.weight = weight
        self.nickname = nickname
    
    #other ways to create a pokemon
    @classmethod
    def from_name(cls, name, a, d, h, level, num_upgrades = None, catch_date = None, 
                move1_num = None, move1_name = None, move2_num = None, move2_name = None,
                height = None, weight = None, nickname = None):
        for i in range(1, 152):
            if base_stat[i]['name'] == name:
                return cls(i, a, d, h, level, num_upgrades, catch_date, 
                move1_num, move1_name, move2_num, move2_name,
                height, weight, nickname)
        raise ValueError('No pokemon found with name: {}'.format(name))
        
    @classmethod
    def from_cp(cls, num, a, d, h, cp, num_upgrades = None, catch_date = None, 
                move1_num = None, move1_name = None, move2_num = None, move2_name = None,
                height = None, weight = None, nickname = None):
        for lv in range(2,79):
            if cls(num, a, d, h, lv/2).get_cp() == cp:
                return cls(num, a, d, h, lv/2, num_upgrades, catch_date, 
                move1_num, move1_name, move2_num, move2_name,
                height, weight, nickname)
        raise ValueError('No {} found with CP: {}'.format(base_stat[num]['name'],cp))
        
    
    def get_level(self):
        return self.level
        
    def get_cp(self):
        if self.cp is not None:
            return self.cp
        _a = (base_stat[self.num]['atk'] + self.a) * cp_mul[self.level_idx]
        _d = (base_stat[self.num]['def'] + self.d) * cp_mul[self.level_idx]
        _h = (base_stat[self.num]['hp'] + self.h) * cp_mul[self.level_idx]
        self.cp = max(10, int(pow(_h, 0.5) * _a * pow(_d, 0.5) / 10))
        return self.cp
        
    def get_stardust_cost(self):
        if self.total_stardust_cost is not None:
            return self.total_stardust_cost
        self.total_stardust_cost = sd_cost[self.level_idx]
        return self.total_stardust_cost

    def get_candy_cost(self):
        if self.total_candy_cost is not None:
            return self.total_candy_cost
        self.total_candy_cost = candy_cost[self.level_idx]
        return self.total_candy_cost
    
    def get_total_stardust_cost(self):
        if self.num_upgrades is None:
            print('The pokemon you created does not contain enough information to calculate total stardust cost')
            return 0
        return self.get_stardust_cost()-Pokemon(self.num, self.a, self.d, self.h, self.level - self.num_upgrades * 0.5).get_stardust_cost()
  
def total_stardust_cost(file, verbose = True):
    all_pkm_raw = json.loads(open(file).read())
    all_pokemon = [Pokemon.from_cp(pkm['pokemon_id'], pkm['iv_attack'], pkm['iv_defence'], pkm['iv_stamina'], 
                               pkm['cp'], pkm['num_upgrades'], pkm['catch_date'], pkm['move1'], pkm['move1_en'],
                               pkm['move2'], pkm['move2_en'], pkm['height'], pkm['weight'], pkm['nickname'])
               for pkm in all_pkm_raw]
    if verbose:
        powered = []
        for pkm in all_pokemon:
            if pkm.get_total_stardust_cost() != 0:
                powered.append([base_stat[pkm.num]['name'], "CP:", pkm.get_cp(), pkm.move1_name, pkm.move2_name, pkm.level, pkm.get_total_stardust_cost()])
        powered.sort(key=lambda x:x[-1], reverse=True)
        pprint.pprint(powered)
    return sum([pkm.get_total_stardust_cost() for pkm in all_pokemon])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PokemonGO calculation tools.') 
    parser.add_argument('-f', '--file', type=str, required=True, help='json file from pokeiv.net')
    parser.add_argument('-s', '--stardust', action='store_true', help='calculate all stardust cost')
    args = parser.parse_args()
    if args.stardust is True:
        print("Total Cost: ", total_stardust_cost(args.file))
    else:
        parser.print_help()