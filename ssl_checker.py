import ssl
import socket
import datetime
from urllib.parse import urlparse
from idna import encode

def punycode_encode(domain):
    return encode(domain).decode('utf-8')

def get_certificate_expiry_date(hostname, port=443):
    context = ssl.create_default_context()
    try:
        conn = context.wrap_socket(socket.create_connection((hostname, port)), server_hostname=hostname)
        cert = conn.getpeercert()
        conn.close()
        cert_expiry_date = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
        days_until_expiry = (cert_expiry_date - datetime.datetime.utcnow()).days
        return days_until_expiry
    except Exception as e:
        return f"Error: {str(e)}"

def check_ssl_expiry(domains):
    results = []

    for domain in domains:
        punycode_domain = punycode_encode(domain)
        days_until_expiry = get_certificate_expiry_date(punycode_domain)
        results.append((domain, days_until_expiry))

    sorted_results = sorted(results, key=lambda x: (float('inf') if isinstance(x[1], str) else x[1], x[0]))
    return sorted_results

if __name__ == "__main__":
    domains = [
        'sto-good.ru',
        'automotor-center.ru',
        'remont-turbin.info',
        'sto-top.ru',
        'домен-с-кириллицей.рф',
        'мох.москва'
    ]

    sorted_results = check_ssl_expiry(domains)

    print("\nSSL Certificate Expiry Check:")
    for result in sorted_results:
        if isinstance(result[1], int):
            print(f"{result[0]} - {result[1]} days until expiry")
        else:
            print(f"{result[0]} - {result[1]}")
