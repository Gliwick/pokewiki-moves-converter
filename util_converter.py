names_converter = dict()
names_file = open('pokenames.csv')

for s in names_file:
	s = s.strip().split(',')
	if len(s) >= 3:
		names_converter[s[1].strip('"')] = s[2].strip('"')

def convert_name(name_en):
    return names_converter.get(name_en, name_en)

types_converter = {
    'Bug': 'Насекомый',
    'Dark': 'Тёмный',
    'Dragon': 'Драконий',
    'Electric': 'Электрический',
    'Fairy': 'Волшебный',
    'Fighting': 'Боевой',
    'Fire': 'Огненный',
    'Flying': 'Летающий',
    'Ghost': 'Призрачный',
    'Grass': 'Травяной',
    'Ground': 'Земляной',
    'Ice': 'ледяной',
    'Normal': 'Нормальный',
    'Poison': 'Ядовитый',
    'Psychic': 'Психический',
    'Rock': 'Каменный',
    'Steel': 'Стальной',
	'Water': 'Водный',
}

def convert_type(type_en):
    return types_converter.get(type_en, type_en)
