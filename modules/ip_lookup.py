import requests
import json
from core.output import print_info, print_success, print_error, create_table

def investigate(ip, args):
    results = {"ip": ip, "services": []}
    
    print_info(f"Начинаем разведку по IP: {ip}")
    
    try:
        # IPAPI.co (бесплатный)
        response = requests.get(f"http://ipapi.co/{ip}/json/", timeout=10)
        geo_data = response.json()
        
        if 'error' not in geo_data:
            results["geolocation"] = {
                "country": geo_data.get("country_name"),
                "city": geo_data.get("city"),
                "region": geo_data.get("region"),
                "isp": geo_data.get("org"),
                "asn": geo_data.get("asn"),
                "latitude": geo_data.get("latitude"),
                "longitude": geo_data.get("longitude")
            }
            
            table_data = [
                ["Страна", geo_data.get("country_name", "N/A")],
                ["Город", geo_data.get("city", "N/A")],
                ["Регион", geo_data.get("region", "N/A")],
                ["Провайдер", geo_data.get("org", "N/A")],
                ["ASN", geo_data.get("asn", "N/A")],
                ["Координаты", f"{geo_data.get('latitude')}, {geo_data.get('longitude')}"]
            ]
            create_table("Геолокация IP", ["Параметр", "Значение"], table_data)

        # Проверка открытых портов через hackertarget.com
        print_info("Проверка открытых портов...")
        try:
            response = requests.get(f"https://api.hackertarget.com/nmap/?q={ip}", timeout=15)
            if "error" not in response.text.lower() and response.text.strip():
                results["port_scan"] = response.text.split("\n")
                print_success(f"Найдено {len(response.text.splitlines())} открытых портов")
                if args.verbose:
                    for line in response.text.splitlines():
                        if line.strip():
                            print_info(f"  {line}")
        except:
            print_error("Не удалось проверить порты")

        # Информация о IP через ipinfo.io
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
            ipinfo_data = response.json()
            if "ip" in ipinfo_data:
                results["ipinfo"] = ipinfo_data
                print_success(f"Hostname: {ipinfo_data.get('hostname', 'N/A')}")
        except:
            pass

        return results
        
    except Exception as e:
        print_error(f"Ошибка: {e}")
        return results