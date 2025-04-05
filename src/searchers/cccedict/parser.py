#A parser for the CC-Cedict. Convert the Chinese-English dictionary into a list of python dictionaries with "traditional","simplified", "pinyin", and "english" keys.

#Make sure that the cedict_ts.u8 file is in the same folder as this file, and that the name matches the file name on line 13.

#Before starting, open the CEDICT text file and delete the copyright information at the top. Otherwise the program will try to parse it and you will get an error message.

#Characters that are commonly used as surnames have two entries in CC-CEDICT. This program will remove the surname entry if there is another entry for the character. If you want to include the surnames, simply delete lines 59 and 60.

#This code was written by Franki Allegra in February 2020.

#open CEDICT file
import os
from pathlib import Path

#define functions

def parse_line(line):
        parsed = {}
        line = line.rstrip('/')
        line = line.split('/')
        if len(line) <= 1:
            return 0
        english = line[1]
        char_and_pinyin = line[0].split('[')
        characters = char_and_pinyin[0]
        characters = characters.split()
        traditional = characters[0]
        simplified = characters[1]
        pinyin = char_and_pinyin[1]
        pinyin = pinyin.rstrip()
        pinyin = pinyin.rstrip("]")
        parsed['traditional'] = traditional
        parsed['simplified'] = simplified
        parsed['pinyin'] = pinyin
        parsed['english'] = english
        return parsed

def remove_surnames(list_hanzi):
    for x in range(len(list_hanzi) - 1, 0, -1):
        if "surname " in list_hanzi[x]['english']:
            if list_hanzi[x]['traditional'] == list_hanzi[x + 1]['traditional']:
                list_hanzi.pop(x)


def get_list() -> list:
    list_hanzi = []
    file_path = Path(__file__).parent.resolve().joinpath("cedict_ts.u8")
    with open(file_path, 'r',  encoding='UTF-8') as file:
        lines = file.read().split('\n')  # Já retorna uma lista

    print("Parsing dictionary . . .")
    for line in lines:
        # Ignora linhas de comentário ou vazias
        if line.startswith('#') or not line.strip():
            continue

        # Processa apenas linhas válidas
        parsed_entry = parse_line(line)  # Corrigido: passa apenas a linha
        if parsed_entry:  # Garante que a entrada não seja None
            list_hanzi.append(parsed_entry)

    print("Removing Surnames . . .")
    remove_surnames(list_hanzi)
    return list_hanzi


        #If you want to save to a database as JSON objects, create a class Word in the Models file of your Django project:

        # print("Saving to database (this may take a few minutes) . . .")
        # for one_dict in list_of_dicts:
        #     new_word = Word(traditional = one_dict["traditional"], simplified = one_dict["simplified"], english = one_dict["english"], pinyin = one_dict["pinyin"], hsk = one_dict["hsk"])
        #     new_word.save()

