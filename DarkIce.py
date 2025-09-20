#!/usr/bin/env python3
"""
DarkIce OSINT Framework - Ultimate Recon Tool
"""

import sys
from core.banner import show_banner
from core.argument_parser import parse_args
from core.output import print_info, print_error, print_success, save_results

def main():
    # Показываем баннер
    show_banner()

    # Парсим аргументы
    args = parse_args()

    # Проверка на помощь
    if hasattr(args, 'help') and args.help:
        print_info("Использование: python darkice.py -t ЦЕЛЬ [МОДУЛИ]")
        print_info("Пример: python darkice.py -t example.com --all --verbose")
        sys.exit(0)

    if not any(vars(args).values()):
        print_error("Не указаны цели для исследования. Используйте -h для справки.")
        sys.exit(1)

    # Обработка целей из файла
    targets = []
    if args.file:
        try:
            with open(args.file, 'r') as f:
                targets = [line.strip() for line in f.readlines() if line.strip()]
            print_success(f"Загружено {len(targets)} целей из файла")
        except FileNotFoundError:
            print_error(f"Файл {args.file} не найден!")
            sys.exit(1)
        except Exception as e:
            print_error(f"Ошибка чтения файла: {e}")
            sys.exit(1)
    elif args.target:
        targets = [args.target]
    else:
        print_error("Не указана цель для исследования! Используйте -t или -f")
        sys.exit(1)

    if not targets:
        print_error("Не найдено целей для исследования!")
        sys.exit(1)

    all_results = []

    # Определяем какие модули запускать
    modules_to_run = []
    if args.all:
        modules_to_run = ['ip', 'domain', 'username', 'email', 'phone', 'social', 'breach']
    else:
        if args.ip: modules_to_run.append('ip')
        if args.domain: modules_to_run.append('domain')
        if args.username: modules_to_run.append('username')
        if args.email: modules_to_run.append('email')
        if args.phone: modules_to_run.append('phone')
        if args.social: modules_to_run.append('social')
        if args.breach: modules_to_run.append('breach')

    if not modules_to_run:
        print_error("Не выбран ни один модуль для исследования! Используйте --all или выберите модули")
        sys.exit(1)

    print_success(f"Запускаем модули: {', '.join(modules_to_run)}")

    # Обработка каждой цели
    for target in targets:
        print_info(f"\n🔍 Начинаем исследование цели: {target}")
        target_results = {"target": target, "modules": {}}

        try:
            # IP Lookup
            if 'ip' in modules_to_run:
                try:
                    from modules.ip_lookup import investigate as ip_investigate
                    target_results["modules"]["ip_lookup"] = ip_investigate(target, args)
                except Exception as e:
                    print_error(f"Ошибка в модуле IP: {e}")

            # Domain Recon
            if 'domain' in modules_to_run:
                try:
                    from modules.domain_recon import investigate as domain_investigate
                    target_results["modules"]["domain_recon"] = domain_investigate(target, args)
                except Exception as e:
                    print_error(f"Ошибка в модуле Domain: {e}")

            # Username Lookup
            if 'username' in modules_to_run:
                try:
                    from modules.username_lookup import investigate as username_investigate
                    target_results["modules"]["username_lookup"] = username_investigate(target, args)
                except Exception as e:
                    print_error(f"Ошибка в модуле Username: {e}")

            # Email Lookup
            if 'email' in modules_to_run:
                try:
                    from modules.email_lookup import investigate as email_investigate
                    target_results["modules"]["email_lookup"] = email_investigate(target, args)
                except Exception as e:
                    print_error(f"Ошибка в модуле Email: {e}")

            # Phone Lookup
            if 'phone' in modules_to_run:
                try:
                    from modules.phone_lookup import investigate as phone_investigate
                    target_results["modules"]["phone_lookup"] = phone_investigate(target, args)
                except Exception as e:
                    print_error(f"Ошибка в модуле Phone: {e}")

            # Social Media
            if 'social' in modules_to_run:
                try:
                    from modules.social_media import investigate as social_investigate
                    target_results["modules"]["social_media"] = social_investigate(target, args)
                except Exception as e:
                    print_error(f"Ошибка в модуле Social: {e}")

            # Breach Check
            if 'breach' in modules_to_run:
                try:
                    from modules.breach_check import investigate as breach_investigate
                    target_results["modules"]["breach_check"] = breach_investigate(target, args)
                except Exception as e:
                    print_error(f"Ошибка в модуле Breach: {e}")

        except KeyboardInterrupt:
            print_error("\nИсследование прервано пользователем")
            sys.exit(1)
        except Exception as e:
            print_error(f"Критическая ошибка при исследовании {target}: {e}")

        all_results.append(target_results)

    # Сохранение результатов
    if args.output:
        try:
            save_results(all_results, args.output)
        except Exception as e:
            print_error(f"Ошибка сохранения отчета: {e}")
    else:
        try:
            save_results(all_results)
        except Exception as e:
            print_error(f"Ошибка сохранения отчета: {e}")

    print_success("🎯 Исследование завершено!")
    print_info("Результаты сохранены в JSON файл")

if __name__ == "__main__":
    main()