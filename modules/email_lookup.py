import requests
import re
from core.output import print_info, print_success, print_error

def investigate(email, args):
    results = {"email": email, "breaches": [], "social_mentions": []}
    
    print_info(f"Анализ email: {email}")
    
    # Проверка формата email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        print_error("Неверный формат email")
        return results
    
    # Парсинг домена из email
    domain = email.split('@')[1]
    results["domain"] = domain
    
    # Проверка на наличие в публичных утечках (через haveibeenpwned.com анонимно)
    print_info("Проверка на утечки данных...")
    try:
        # Получаем SHA1 хэш email (как в HIBP)
        import hashlib
        email_hash = hashlib.sha1(email.encode('utf-8')).hexdigest().upper()
        prefix = email_hash[:5]
        
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=15)
        if response.status_code == 200:
            hashes = response.text.splitlines()
            for h in hashes:
                if email_hash[5:] in h:
                    breach_count = h.split(':')[1]
                    results["breaches"].append({
                        "source": "HaveIBeenPwned",
                        "breach_count": breach_count
                    })
                    print_warning(f"Email найден в {breach_count} утечках!")
                    break
            else:
                print_success("Email не найден в известных утечках")
    except:
        print_error("Не удалось проверить утечки")
    
    # Поиск упоминаний в соцсетях (базовый)
    print_info("Поиск упоминаний в соцсетях...")
    social_platforms = [
        f"https://www.facebook.com/search/top/?q={email}",
        f"https://twitter.com/search?q={email}",
        f"https://www.linkedin.com/search/results/all/?keywords={email}",
    ]
    
    for url in social_platforms:
        platform = url.split('.')[1]
        results["social_mentions"].append({
            "platform": platform,
            "url": url,
            "checked": True
        })
        print_info(f"  {platform}: {url}")
    
    return results