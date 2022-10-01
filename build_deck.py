import json, os
from typing import Dict, List

output_filepath = os.path.join('output', '今天吃什么.json')
deck_name = '今天吃什么'
HowToCook_Dir = os.path.join('HowToCook', 'dishes')

class Dishes:
    _dishes: Dict[str, List[str]]

    def __init__(self):
        self._dishes = dict()

    def add_deck(self, deck_name: str, lst: List[str], hidden: bool):
        if hidden:
            deck_name = f'_{deck_name}'

        try:
            try_get_dishes = self._dishes[deck_name]
            try_get_dishes.extend(lst)
        except KeyError:
            self._dishes[deck_name] = list(lst)

    def dump_json(self, filename: str):
        json.dump(self._dishes, open(filename, "w", encoding='utf8'), ensure_ascii=False, indent=4)

dishes = Dishes()

dirnames = os.listdir(HowToCook_Dir)
dirnames.remove('template')

for dish_type in dirnames:
    sub_dishes = os.listdir(os.path.join(HowToCook_Dir,dish_type))
    sub_dishes = list(map(lambda file: os.path.splitext(file)[0], sub_dishes))
    dishes.add_deck(dish_type, sub_dishes, True)

dishes.add_deck("今天吃什么", dirnames, False)

dishes.dump_json(output_filepath)
