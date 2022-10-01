import json, os
from typing import Dict, Iterable, List

output_filepath = os.path.join('output', '今天吃什么.json')
HowToCook_Dir = os.path.join('HowToCook', 'dishes')

class Dishes:
    _dishes: Dict[str, List[str]]

    def __init__(self):
        self._dishes = dict()

    def add_deck(self, deck_name: str, lst: Iterable[str], hidden: bool = False):
        if hidden:
            deck_name = f'_{deck_name}'

        try:
            try_get_dishes = self._dishes[deck_name]
            try_get_dishes.extend(lst)
        except KeyError:
            self._dishes[deck_name] = list(lst)
    
    # { "group_name": ["{%放回抽取卡牌}", "{不放回抽取卡牌}"] }
    def add_deck_group(self, group_name: str, lst: Iterable[str], put_back: bool = True, hidden: bool = False):
        if hidden:
            group_name = f'_{group_name}'

        if put_back:
            maped_lst = map(lambda d: f'{{%{d}}}', lst)
        else:
            maped_lst = map(lambda d: f'{{{d}}}', lst)
        try:
            try_get_dishes = self._dishes[group_name]
            try_get_dishes.extend(maped_lst)
        except KeyError:
            self._dishes[group_name] = list(maped_lst)


    def dump_json(self, filename: str):
        json.dump(self._dishes, open(filename, "w", encoding='utf8'), ensure_ascii=False, indent=4)

dishes = Dishes()

dirnames = os.listdir(HowToCook_Dir)
dirnames.remove('template')

for dish_type in dirnames:
    sub_dishes = os.listdir(os.path.join(HowToCook_Dir,dish_type))
    sub_dishes = list(map(lambda file: os.path.splitext(file)[0], sub_dishes))
    dishes.add_deck(dish_type, sub_dishes, True)

dishes.add_deck_group("今天吃什么", filter(lambda x: x not in ['condiment', 'drink'], dirnames))
dishes.add_deck_group("今天喝什么", filter(lambda x: x == 'drink', dirnames))

dishes.add_deck_group("来点酱料", filter(lambda x: x == 'condiment', dirnames))
dishes.add_deck_group("来点快餐", [])

dishes.add_deck_group("早饭吃什么", ['今天吃什么'])
dishes.add_deck_group("午饭吃什么", ['今天吃什么'])
dishes.add_deck_group("晚饭吃什么", ['今天吃什么'])

dishes.dump_json(output_filepath)
