import requests
import hashlib
from core.output import print_info, print_success, print_error

def investigate(target, args):
    results = {"target": target, "breaches": []}
    
    # Определяем тип цели (email или password)
    if '@' in target:
        print_info(f"Проверка email на утечки: {target}")
        return check_email_breach(target)
    else:
        print_info(f"Проверка пароля на утечки: {target[:2]}...")
        return check_password_breach(target)

def check_email_breach(email):
    results = {"type": "email", "breaches": []}
    
    try:
        # Анонимная проверка через HIBP API
        email_hash = hashlib.sha1(email.encode('utf-8')).hexdigest().upper()
        prefix = email_hash[:5]
        
        response = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}",
            headers={'User-Agent': 'DarkIce-OSINT-Scanner'},
            timeout=15
        )
        
        if response.status_code == 200:
            found = False
            for line in response.text.splitlines():
                hash_suffix, count = line.split(':')
                if email_hash[5:] == hash_suffix:
                    results["breaches"].append({
                        "breach_count": int(count),
                        "source": "HaveIBeenPwned"
                    })
                    print_warning(f"⚠️  Email найден в {count} утечках!")
                    found = True
                    break
            
            if not found:
                print_success("✅ Email не найден в известных утечках")
        
    except Exception as e:
        print_error(f"Ошибка проверки утечек: {e}")
    
    return results

def check_password_breach(password):
    results = {"type": "password", "breached": False}
    
    try:
        # Проверка пароля через HIBP
        password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = password_hash[:5]
        
        response = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}",
            headers={'User-Agent': 'DarkIce-OSINT-Scanner'},
            timeout=15
        )
        
        if response.status_code == 200:
            for line in response.text.splitlines():
                hash_suffix, count = line.split(':')
                if password_hash[5:] == hash_suffix:
                    results["breached"] = True
                    results["breach_count"] = int(count)
                    print_error(f"🚨 Пароль найден в {count} утечках! Срочно смени!")
                    return results
            
            print_success("✅ Пароль не найден в утечках")
        
    except Exception as e:
        print_error(f"Ошибка проверки пароля: {e}")
    
    return results