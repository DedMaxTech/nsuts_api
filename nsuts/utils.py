translit_dict = {'ь': '', 'ъ': '', 'а': 'a', 'б': 'b', 'в': 'v',
                 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
                 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l',
                 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
                 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
                 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ы': 'yi',
                 'э': 'e', 'ю': 'yu', 'я': 'ya'}


def translit(x:str):
    '''Транслитерация строки
    >>> translit('Иванов Иван Иванович')
    Ivanov Ivan Ivanovich'''
    t = ''
    for i in x:
        t += translit_dict.get(i.lower(), i.lower()).upper() if i.isupper() else translit_dict.get(i, i)
    return t
