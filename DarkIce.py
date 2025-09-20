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

    if not any(vars(args).values()):
        print_error("Не указаны цели для исследования. Используйте -h для справки.")
        sys.exit(1)

    # Обработка целей из файла
    targets = []
    if args.file:
        try:
            with open(args.file, 'r') as f:
                targets = [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            print_error(f"Файл {args.file} не найден!")
            sys.exit(1)
    elif args.target:
        targets = [args.target]

    if not targets:
        print_error("Не указаны цели для исследования!")
        sys.exit(1)

    all_results = []

    for target in targets:
        print_info(f"\n🔍 Начинаем исследование цели: {target}")
        target_results = {"target": target, "modules": {}}

        # Запуск модулей
        if args.all or args.ip:
            from modules.ip_lookup import investigate as ip_investigate
            target_results["modules"]["ip_lookup"] = ip_investigate(target, args)

        if args.all or args.domain:
            from modules.domain_recon import investigate as domain_investigate
            target_results["modules"]["domain_recon"] = domain_investigate(target, args)

        if args.all or args.username:
            from modules.username_lookup import investigate as username_investigate
            target_results["modules"]["username_lookup"] = username_investigate(target, args)

        if args.all or args.email:
            from modules.email_lookup import investigate as email_investigate
            target_results["modules"]["email_lookup"] = email_investigate(target, args)

        if args.all or args.breach:
            from modules.breach_check import investigate as breach_investigate
            target_results["modules"]["breach_check"] = breach_investigate(target, args)

        if args.all or args.social:
            from modules.social_media import investigate as social_investigate
            target_results["modules"]["social_media"] = social_investigate(target, args)

        all_results.append(target_results)

    # Сохранение результатов
    if args.output:
        save_results(all_results, args.output)
    else:
        save_results(all_results)

    print_success("Исследование завершено! 🎯")

if __name__ == "__main__":
    main()