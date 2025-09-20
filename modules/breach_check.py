import requests
import hashlib
from core.output import print_info, print_success, print_error, print_warning

def investigate(target, args):
    print_info(f"Проверка на утечки данных: {target}")
    
    results = {
        "target": target,
        "breaches": [],
        "leaked": False
    }
    
    try:
        # Для email
        if '@' in target:
            email_hash = hashlib.sha1(target.encode('utf-8')).hexdigest().upper()
            prefix = email_hash[:5]
            
            response = requests.get(
                f"https://api.pwnedpasswords.com/range/{prefix}",
                headers={'User-Agent': 'DarkIce-OSINT-Scanner'},
                timeout=15
            )
            
            if response.status_code == 200:
                for line in response.text.splitlines():
                    if email_hash[5:] in line:
                        count = line.split(':')[1]
                        results["breaches"].append({
                            "source": "HaveIBeenPwned",
                            "count": count
                        })
                        results["leaked"] = True
                        print_warning(f"Найдено в утечках: {count} раз")
                        break
                else:
                    print_success("Не найдено в известных утечках")
        
        # Для паролей
        else:
            password_hash = hashlib.sha1(target.encode('utf-8')).hexdigest().upper()
            prefix = password_hash[:5]
            
            response = requests.get(
                f"https://api.pwnedpasswords.com/range/{prefix}",
                headers={'User-Agent': 'DarkIce-OSINT-Scanner'},
                timeout=15
            )
            
            if response.status_code == 200:
                for line in response.text.splitlines():
                    if password_hash[5:] in line:
                        count = line.split(':')[1]
                        results["breaches"].append({
                            "source": "HaveIBeenPwned",
                            "count": count
                        })
                        results["leaked"] = True
                        print_error(f"Пароль найден в {count} утечках! Срочно смени!")
                        break
                else:
                    print_success("Пароль не найден в утечках")
                    
    except Exception as e:
        print_error(f"Ошибка проверки утечек: {e}")
    
    return results