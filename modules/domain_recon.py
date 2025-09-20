import whois
import dns.resolver
import requests
from bs4 import BeautifulSoup
from core.output import print_info, print_success, print_error, create_table

def investigate(domain, args):
    results = {"domain": domain, "dns_records": {}, "technologies": []}
    
    print_info(f"Начинаем разведку домена: {domain}")
    
    try:
        # WHOIS информация
        try:
            whois_info = whois.whois(domain)
            results["whois"] = {
                "registrar": whois_info.registrar,
                "creation_date": str(whois_info.creation_date),
                "expiration_date": str(whois_info.expiration_date),
                "name_servers": whois_info.name_servers,
                "status": whois_info.status
            }
            
            whois_data = [
                ["Регистратор", whois_info.registrar or "N/A"],
                ["Дата создания", str(whois_info.creation_date) if whois_info.creation_date else "N/A"],
                ["Дата истечения", str(whois_info.expiration_date) if whois_info.expiration_date else "N/A"],
                ["Статус", ", ".join(whois_info.status) if whois_info.status else "N/A"]
            ]
            create_table("WHOIS информация", ["Параметр", "Значение"], whois_data)
        except:
            print_error("Не удалось получить WHOIS информацию")
        
        # DNS записи
        print_info("Получение DNS записей...")
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        dns_data = []
        
        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                records = [str(r) for r in answers]
                results["dns_records"][rtype] = records
                dns_data.append([rtype, "\n".join(records)])
            except:
                results["dns_records"][rtype] = []
        
        if dns_data:
            create_table("DNS записи", ["Тип", "Значение"], dns_data)
        
        # HTTP информация
        print_info("Анализ HTTP заголовков...")
        try:
            response = requests.get(f"http://{domain}", timeout=10, allow_redirects=True)
            results["http"] = {
                "status_code": response.status_code,
                "final_url": response.url,
                "headers": dict(response.headers),
                "server": response.headers.get('Server', 'N/A'),
                "content_type": response.headers.get('Content-Type', 'N/A')
            }
            
            http_data = [
                ["Статус", str(response.status_code)],
                ["Сервер", response.headers.get('Server', 'N/A')],
                ["Тип контента", response.headers.get('Content-Type', 'N/A')],
                ["Размер", f"{len(response.content)} bytes"]
            ]
            create_table("HTTP информация", ["Параметр", "Значение"], http_data)
            
        except Exception as e:
            print_error(f"Ошибка HTTP запроса: {e}")
        
        # Поиск поддоменов через hackertarget.com
        if args.verbose:
            print_info("Поиск поддоменов...")
            try:
                response = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=15)
                if "error" not in response.text.lower() and response.text.strip():
                    subdomains = [line.split(',')[0] for line in response.text.splitlines() if line.strip()]
                    results["subdomains"] = subdomains
                    print_success(f"Найдено {len(subdomains)} поддоменов")
                    if subdomains:
                        for sub in subdomains[:5]:  # Показываем первые 5
                            print_info(f"  {sub}")
            except:
                print_error("Не удалось получить поддомены")
        
        return results
        
    except Exception as e:
        print_error(f"Ошибка анализа домена: {e}")
        return results