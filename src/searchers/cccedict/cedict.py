from typing import List, Dict
from src import Searcher, Hanzi,Info
from .parser import get_list

def clean_extra_hanzi(hanzi_info: dict, text: str):
    mul_hanzi_word_position = {}
    ## get the chinese words and sort them by length
    hanzi_definitions = sorted([hanzi for hanzi in hanzi_info.values()], key=lambda x: len(x.simplified), reverse=True)
    for hanzi in hanzi_definitions:
        if any(hanzi in seed_hanzi for seed_hanzi in mul_hanzi_word_position.values()):
            continue
        positions_to_remove: List = []
        #find hanzi chars position to find where is the position of the word in the text
        for sim_chars, tra_chars in hanzi.hanzi_iterator():

            if sim_chars in text:
                positions_to_remove.append(text.index(sim_chars))
                continue
            if tra_chars in text:
                positions_to_remove.append(text.index(tra_chars))
                continue
        print(hanzi.simplified)

        if len(positions_to_remove) > 1:
            positions_to_remove.sort()
            #need to add filter system for nor crescent numbers
            positions_to_remove = [positions_to_remove[pos] for pos in range(0,len(positions_to_remove)) if positions_to_remove[pos] == positions_to_remove[pos-1]+1]
        print(f"posição de hanzi: {hanzi.simplified} --- {positions_to_remove[0]}")
        mul_hanzi_word_position[positions_to_remove[0]] = hanzi
    return mul_hanzi_word_position

def extract_info_from_source(text:str) -> dict:
    seen = {}
    for info in get_list():
        if info['simplified'] in text or info['traditional'] in text:
            if info['simplified'] in seen or info['traditional'] in seen:
                seen[info['simplified']].add_description(info['english'])
                continue
            seen[info['simplified']] = Hanzi(
                simplified=info['simplified'],
                traditional=info['traditional'],
                pinyin=info['pinyin'],
                description=[info['english']]
            )
    return seen


class Cedict(Searcher):
    def search_meaning(self, text: str):
        source_info = extract_info_from_source(text)
        source_info = clean_extra_hanzi(source_info,text)
        return [info for _,info in sorted(source_info.items())]


