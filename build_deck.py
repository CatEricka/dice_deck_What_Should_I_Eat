from collections import OrderedDict
import json, os
from typing import Dict, Iterable, List, Set, Tuple

output_filepath = os.path.join('output', '今天吃什么.json')
HowToCook_Dir = os.path.join('HowToCook', 'dishes')

class Deck:
    _hidden: bool
    _deck_name: str
    _cards: List[str]

    def __init__(self, deck_name: str, cards: Iterable[str], hidden: bool = False):
        self._hidden = hidden
        self._cards = list(cards)
        self._deck_name = deck_name

    def get_real_deck_name(self):
        return self._deck_name
    
    def get_deck_name_mangling(self):
        if self._hidden:
            return f'_{self._deck_name}'
        else:
            return self._deck_name

    def get_cards_copied(self):
        return list(self._cards)

    def is_hidden(self):
        return self._hidden

    def merge(self, other):
        if id(self) == id(other):
            return
        elif isinstance(other, self.__class__):
            if self.get_deck_name_mangling() == other.get_deck_name_mangling():
                self._cards.extend(other._cards)
            self._hidden = self._hidden or other._hidden

    def dump(self) -> Tuple[str, List[str]]:
        return (self.get_deck_name_mangling(), self.get_cards_copied())

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, self.__class__):
            return self._deck_name == __o._deck_name
        else:
            return False
    
    def __hash__(self) -> int:
        return hash(self._deck_name)

class DeckGroup:
    _hidden: bool
    _group_name: str
    # [(卡组, True放回/False不放回), ...]
    _deck_refs: List[Tuple[Deck, bool]]

    def __init__(self, group_name: str, hidden: bool = False) -> None:
        self._hidden = hidden
        self._group_name = group_name
        self._deck_refs = list()

    def add_deck(self, deck: Deck | None, put_back: bool = True):
        if deck:
            self._deck_refs.append((deck, put_back))
        return self

    def extend_deck(self, deck_refs:  Iterable[Deck], put_back: bool = True):
        self._deck_refs.extend(map(lambda d: (d, put_back), deck_refs))
        return self

    def get_real_deck_group_name(self):
        return self._group_name
    
    def get_deck_group_name_mangling(self):
        if self._hidden:
            return f'_{self._group_name}'
        else:
            return self._group_name
    
    def merge(self, other):
        if id(self) == id(other):
            return self
        elif isinstance(other, self.__class__):
            if self._group_name == other._group_name:
                self._deck_refs.extend(other._deck_refs)
                self.hidden = self.hidden or other.hidden
        return self

    def dump(self) -> Tuple[str, List[str]]:
        lst = list()
        for (deck, put_back) in self._deck_refs:
            if put_back:
                lst.append(f'{{%{deck.get_deck_name_mangling()}}}')
            else:
                lst.append(f'{{{deck.get_deck_name_mangling()}}}')
        return (self.get_deck_group_name_mangling(), lst)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, self.__class__):
            return self._group_name == __o._group_name
        else:
            return False
    
    def __hash__(self) -> int:
        return hash(self._group_name)

class ComposeGroup:
    _hidden: bool
    _compose_group_name: str
    # [(其它复合组, True放回/False不放回), ...]
    _refs: List[Tuple[DeckGroup, bool]]

    def __init__(self, group_name:str, hidden: bool = False):
        self._hidden = hidden
        self._compose_group_name = group_name
        self._refs = list()

    def add_deck_group(self, group: DeckGroup | None, put_back: bool = True):
        if group:
            self._refs.append((group, put_back))
        return self

    def extend_deck_groups(self, groups:  Iterable[DeckGroup], put_back: bool = True):
        self._refs.extend(map(lambda d: (d, put_back), groups))
        return self

    def get_real_compose_group_name(self):
        return self._compose_group_name

    def get_compose_group_name_mangling(self):
        if self._hidden:
            return f'_{self._compose_group_name}'
        else:
            return self._compose_group_name

    def dump(self) -> Tuple[str, List[str]]:
        lst = list()
        for (group, put_back) in self._refs:
            if put_back:
                lst.append(f'{{%{group.get_deck_group_name_mangling()}}}')
            else:
                lst.append(f'{{{group.get_deck_group_name_mangling()}}}')
        return (self.get_compose_group_name_mangling(), lst)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, self.__class__):
            return self._compose_group_name == __o._compose_group_name
        else:
            return False
    
    def __hash__(self) -> int:
        return hash(self._compose_group_name)

class Dishes:
    decks: Set[Deck]
    deck_groups: Set[DeckGroup]
    compose_group: Set[ComposeGroup]

    def __init__(self):
        self.decks = set()
        self.deck_groups = set()
        self.compose_group = set()

    def add_deck(self, deck: Deck):
        self.decks.add(deck)
        return self
    
    def add_group(self, deck_group: DeckGroup | ComposeGroup):
        if not deck_group:
            return self
        if isinstance(deck_group, DeckGroup):
            self.deck_groups.add(deck_group)
        elif isinstance(deck_group, ComposeGroup):
            self.compose_group.add(deck_group)
        return self

    def get_deck_by_name(self, name: str) -> Deck | None:
        for deck in self.decks:
            if deck._deck_name == name:
                return deck
        return None
    
    def get_deck_group_by_name(self, name: str) -> DeckGroup | None:
        for group in self.deck_groups:
            if group.get_real_deck_group_name() == name:
                return group
        return None
    
    def get_compose_group_by_name(self, name: str) -> ComposeGroup | None:
        for group in self.compose_group:
            if group.get_real_compose_group_name() == name:
                return group
        return None

    def get_decks_not_in(self, decks_name: List[str]) -> Iterable[Deck]:
        return filter(lambda deck: deck.get_deck_name_mangling() not in decks_name, self.decks)

    def get_decks_group_not_in(self, deck_group_names: List[str]) -> Iterable[DeckGroup]:
        return filter(lambda deck_group: deck_group.get_deck_group_name_mangling() not in deck_group_names, self.deck_groups)
    
    def get_compose_group_not_in(self, compose_group_names: List[str]) -> Iterable[ComposeGroup]:
        return filter(lambda deck_group: deck_group.get_real_compose_group_name() not in compose_group_names, self.compose_group)

    def dump_json(self, filename: str):
        output = dict()
        for deck in self.decks:
            d = deck.dump()
            output[d[0]] = sorted(d[1])
        for group in self.deck_groups:
            g = group.dump()
            output[g[0]] = sorted(g[1])
        for group in self.compose_group:
            g = group.dump()
            output[g[0]] = sorted(g[1])
        with open(filename, "w", encoding='utf8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4, sort_keys=True)


# 实例
DISHES = Dishes()

# HowToCook 菜单
dirnames = os.listdir(HowToCook_Dir)
dirnames.remove('template')
for dish_type in dirnames:
    sub_dishes = os.listdir(os.path.join(HowToCook_Dir,dish_type))
    sub_dishes = list(map(lambda file: os.path.splitext(file)[0], sub_dishes))
    DISHES.add_deck(Deck(dish_type, sub_dishes, True))

# 今日之选
TODAYS_CHOSEN = DeckGroup('今天吃什么').extend_deck(DISHES.get_decks_not_in(['condiment', 'drink']))
DISHES.add_group(TODAYS_CHOSEN)


# 其它分组
DISHES.add_group(DeckGroup('今天喝什么').add_deck(DISHES.get_deck_by_name('drink')))
DISHES.add_group(DeckGroup('来点酱料').add_deck(DISHES.get_deck_by_name('condiment')))

# 复合分组
DISHES.add_group(ComposeGroup("早饭吃什么").add_deck_group(DISHES.get_deck_group_by_name('今天吃什么')))
DISHES.add_group(ComposeGroup("午饭吃什么").add_deck_group(DISHES.get_deck_group_by_name('今天吃什么')))
DISHES.add_group(ComposeGroup("晚饭吃什么").add_deck_group(DISHES.get_deck_group_by_name('今天吃什么')))


def load_external_dishes(file_name: str, group_name: str | None = None, add_to_todays_chosen = True):
    '''
    file_name:
        `mixin` 目录下 json 文件路径, 文件名会作为新卡组名
    group_name:
        新分组名, 如果不为 `None`, 卡组自身会被隐藏, 只是用分组名作为公开卡组
    add_to_todays_chosen:
        是否添加到总分组 `今天吃什么`
    '''
    with open(os.path.join('mixins', file_name), 'r', encoding='utf8') as f:
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        extern_dishes = Deck(base_name, json.load(f), True)

        DISHES.add_deck(extern_dishes)
        if group_name:
            DISHES.add_group(DeckGroup(group_name).add_deck(extern_dishes))

        # 添加到今日之选
        if add_to_todays_chosen:
            TODAYS_CHOSEN.add_deck(extern_dishes)

# 其它来源
load_external_dishes('快餐.json', group_name='来点快餐', add_to_todays_chosen=True)

DISHES.dump_json(output_filepath)
