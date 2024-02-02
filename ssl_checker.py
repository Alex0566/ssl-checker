import ssl
import socket
import datetime

def get_certificate_expiry_date(hostname, port=443):
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.create_connection((hostname, port)), server_hostname=hostname)
    cert = conn.getpeercert()
    conn.close()
    cert_expiry_date = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
    days_until_expiry = (cert_expiry_date - datetime.datetime.utcnow()).days
    return days_until_expiry

def check_ssl_expiry(domains):
    results = []

    for domain in domains:
        try:
            days_until_expiry = get_certificate_expiry_date(domain)
            results.append((domain, days_until_expiry))
        except Exception as e:
            results.append((domain, "Error: " + str(e)))

    sorted_results = sorted(results, key=lambda x: x[1])
    return sorted_results

if __name__ == "__main__":
    domains = [
        'sto-good.ru',
        'automotor-center.ru',
        'remont-turbin.info',
        'sto-top.ru'
    ]

    sorted_results = check_ssl_expiry(domains)

    print("\nSSL Certificate Expiry Check:")
    for result in sorted_results:
        if isinstance(result[1], int):
            print(f"{result[0]} - {result[1]} days until expiry")
        else:
            print(f"{result[0]} - {result[1]}")
