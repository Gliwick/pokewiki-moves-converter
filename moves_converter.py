from util_converter import convert_name, convert_type

input_file = open('moves_en.txt')
output_file = open('moves_ru.txt', 'w')
output = []

try:
    for s in input_file.readlines():
        s = s.strip()
        if s.strip('=') == 'Learnset':
            output.append('==Изучение==')
            continue
        if s.strip('=') == 'By [[Level|leveling up]]':
            output.append('==При [[Уровень|повышении уровня]]==')
            continue

        if s.startswith('{{'):
            s = s[2:]
        if s.endswith('}}'):
            s = s[:-2]

        params_en = s.split('|')
        params_ru = []
        if params_en[0] == 'Movehead/Level':
            params_ru.append('Приемышапка/уровень')
            params_ru.append(convert_type(params_en[1]))
            params_ru.append('1')

        elif params_en[0] == 'Movefoot':
            params_ru.append('Приемыниз')
            params_ru.append(convert_type(params_en[1]))
            params_ru.append('1')

        elif params_en[0] == 'Moveentry/7':
            params_ru.append('Приемы/Поколение1')
            params_ru.append(params_en[1]) # dex number
            params_ru.append(convert_name(params_en[2])) # name

            dual_type = params_en[4].startswith('type2=')

            type1 = params_en[3].split('=')
            if len(type1) > 1:
                type1 = type1[1]
            else:
                type1 = type1[0]

            if dual_type:
                type2 = params_en[4].split('=')[1]
            else:
                type2 = type1[:]

            params_ru.append(str(1 + int(dual_type))) # number of types
            params_ru.append(convert_type(type1))
            params_ru.append(convert_type(type2))

            len_without_levels = len(params_ru)
            subparams_ru = ['']

            params_en[7 + int(dual_type)] = '|'.join(params_en[7 + int(dual_type):]) + '|'
            tag_mode = False
            previous = ''
            for c in params_en[7 + int(dual_type)]:

                if c == '{' and previous == '{':
                    subparams_ru[-1] = subparams_ru[-1].rstrip('{')
                    tag = ''
                    tag_mode = True
                if c == '}' and previous == '}':
                    if not tag_mode:
                        break
                    if tag.rstrip('}').strip() == 'Learned upon evolving':
                        subparams_ru[-1] += '{{tt|ЭВ|Изучается при эволюции}}'
                    else:
                        subparams_ru[-1] = '{{tt|' + subparams_ru[-1].replace('{{tt|ЭВ|Изучается при эволюции}}', 'ЭВ') + '|' + tag + '}}'
                    tag_mode = False
                if previous == '>' and subparams_ru[-1].endswith('<br>') and not tag_mode:
                    subparams_ru[-1] = subparams_ru[-1].replace('<br>', '')
                    subparams_ru.append('')

                if c != '{' and c != '}':
                    if tag_mode:
                        if c == '|':
                            tag = ''
                        else:
                            tag += c

                    if not tag_mode:
                        if c == '|':
                            param = '/'.join(subparams_ru)
                            subparams_ru = ['']
                            if param.startswith('STAB='):
                                continue
                            if len(param) == 0:
                                param = '-'
                            param = param.replace('Evo.', 'ЭВ')
                            params_ru.append(param)
                            if len(params_ru) == len_without_levels + 7:
                                break
                        else:
                            subparams_ru[-1] += c

                previous = c


        if params_ru:
            output.append('{{' + '|'.join(params_ru) + '}}')
        else:
            output.append(s)

    for s in output:
        output_file.write(s + '\n')

except Exception as e:
    output_file.write('Произошла ошибка при обработке строки:\n')
    output_file.write(s + '\n\n')
    output_file.write('Сообщите Джону вместе с кодом ошибки:\n')
    output_file.write(str(e))
