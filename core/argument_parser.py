import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="DarkIce OSINT Framework", add_help=False)
    
    # Основные аргументы
    main_group = parser.add_argument_group("Main Arguments")
    main_group.add_argument("-t", "--target", help="Цель для исследования")
    main_group.add_argument("-f", "--file", help="Файл со списком целей")
    main_group.add_argument("-o", "--output", help="Сохранить отчет в файл")
    
    # Модули
    modules_group = parser.add_argument_group("Modules")
    modules_group.add_argument("-all", "--all", action="store_true", help="Запустить все модули")
    modules_group.add_argument("-ip", "--ip", action="store_true", help="Разведка по IP")
    modules_group.add_argument("-d", "--domain", action="store_true", help="Разведка домена")
    modules_group.add_argument("-u", "--username", action="store_true", help="Поиск по username")
    modules_group.add_argument("-e", "--email", action="store_true", help="Поиск по email")
    modules_group.add_argument("-p", "--phone", action="store_true", help="Поиск по телефону")
    modules_group.add_argument("-s", "--social", action="store_true", help="Поиск в соцсетях")
    modules_group.add_argument("-b", "--breach", action="store_true", help="Проверка на утечки")
    
    # Опции
    options_group = parser.add_argument_group("Options")
    options_group.add_argument("-v", "--verbose", action="store_true", help="Подробный вывод")
    options_group.add_argument("-h", "--help", action="help", help="Показать помощь")
    
    return parser.parse_args()