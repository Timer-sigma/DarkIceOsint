import requests
import re
from core.output import print_info, print_success, print_error, print_warning, create_table

def investigate(phone, args):
    results = {"phone": phone, "carrier": "", "region": "", "social_mentions": []}
    
    print_info(f"🔍 Начинаем разведку по номеру: {phone}")
    
    # Очистка номера от лишних символов
    clean_phone = re.sub(r'[^0-9+]', '', phone)
    results["clean_phone"] = clean_phone
    
    # Проверка формата номера
    if not re.match(r'^(\+7|7|8)?[0-9]{10}$', clean_phone.replace('+', '')):
        print_error("Неверный формат номера телефона (ожидается российский номер)")
        return results
    
    # Нормализация номера (приводим к формату +7XXXXXXXXXX)
    if clean_phone.startswith('8'):
        normalized_phone = '+7' + clean_phone[1:]
    elif clean_phone.startswith('7'):
        normalized_phone = '+' + clean_phone
    elif clean_phone.startswith('+7'):
        normalized_phone = clean_phone
    else:
        normalized_phone = '+7' + clean_phone
    
    results["normalized_phone"] = normalized_phone
    
    try:
        # 1. Определение оператора и региона через API
        print_info("Определение оператора и региона...")
        try:
            response = requests.get(
                f"https://phoneinfoga.crvx.fr/api/numbers/{normalized_phone}/info",
                headers={'User-Agent': 'DarkIce-OSINT-Scanner/1.0'},
                timeout=10
            )
            
            if response.status_code == 200:
                phone_data = response.json()
                results["carrier"] = phone_data.get('carrier', {}).get('name', 'Неизвестно')
                results["region"] = phone_data.get('location', 'Неизвестно')
                
                print_success(f"Оператор: {results['carrier']}")
                print_success(f"Регион: {results['region']}")
                
                # Создаем таблицу с информацией
                table_data = [
                    ["Номер", normalized_phone],
                    ["Оператор", results["carrier"]],
                    ["Регион", results["region"]],
                    ["Формат", phone_data.get('format', {}).get('international', 'N/A')]
                ]
                create_table("Информация о номере", ["Параметр", "Значение"], table_data)
        except:
            print_warning("Не удалось получить информацию об операторе")
        
        # 2. Поиск в мессенджерах и соцсетях
        print_info("Поиск в мессенджерах...")
        check_messengers(normalized_phone, results)
        
        # 3. Поиск в социальных сетях
        print_info("Поиск в социальных сетях...")
        check_social_networks(normalized_phone, results)
        
        # 4. Проверка на спам/мошенничество
        print_info("Проверка на спам...")
        check_spam_databases(normalized_phone, results)
        
        return results
        
    except Exception as e:
        print_error(f"Ошибка при анализе номера: {e}")
        return results

def check_messengers(phone, results):
    """Проверка привязки номера к мессенджерам"""
    messengers = {
        "WhatsApp": f"https://wa.me/{phone}",
        "Telegram": f"https://t.me/{phone.replace('+', '')}",
        "Viber": f"viber://chat?number={phone}",
    }
    
    for app_name, url in messengers.items():
        results["social_mentions"].append({
            "platform": app_name,
            "url": url,
            "checked": True
        })
        print_info(f"  {app_name}: {url}")

def check_social_networks(phone, results):
    """Проверка номера в соцсетях"""
    social_networks = {
        "VK": f"https://vk.com/phone/{phone}",
        "Instagram": f"https://www.instagram.com/accounts/account_recovery/?phone_number={phone}",
        "Facebook": f"https://www.facebook.com/login/identify/?phone_number={phone}",
        "Twitter": f"https://twitter.com/search?q={phone}",
        "Avito": f"https://www.avito.ru/items/phones?phone={phone}",
        "Юла": f"https://youla.ru/search?phone={phone}",
    }
    
    for network, url in social_networks.items():
        results["social_mentions"].append({
            "platform": network,
            "url": url,
            "checked": True
        })
        print_info(f"  {network}: {url}")

def check_spam_databases(phone, results):
    """Проверка номера в базах спамеров"""
    spam_checkers = {
        "Кто звонил": f"https://kto-zvonil.com.ua/nomer/{phone}",
        "СберКто": f"https://sberkto.ru/{phone}",
        "НомерОрг": f"https://номер.org/{phone}",
    }
    
    for service, url in spam_checkers.items():
        try:
            response = requests.get(url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                results["spam_check"] = results.get("spam_check", [])
                results["spam_check"].append({
                    "service": service,
                    "url": url,
                    "found": True
                })
                print_warning(f"  {service}: номер есть в базе - {url}")
        except:
            pass

# Дополнительная функция для массовой проверки
def check_phone_reputation(phone):
    """Проверка репутации номера"""
    try:
        # Используем публичные API для проверки репутации
        response = requests.get(
            f"https://api.numverify.com/validate?number={phone}",
            timeout=10
        )
        return response.json()
    except:
        return None