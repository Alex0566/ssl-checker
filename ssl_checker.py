import ssl
import socket
from datetime import datetime

def check_ssl_expiry(domain, port=443):
    try:
        context = ssl.create_default_context()
        with context.wrap_socket(socket.create_connection((domain, port)), server_hostname=domain) as sock:
            cert = sock.getpeercert()
            expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            days_left = (expiry_date - datetime.now()).days
            return days_left
    except Exception as e:
        return str(e)

def main():
    domains = """
    sto-good.ru
    automotor-center.ru
    remont-turbin.info
    sto-top.ru
    """.split()

    for domain in domains:
        days_left = check_ssl_expiry(domain)
        print(f"Days left for {domain}: {days_left} days")
        # Добавьте здесь логику уведомлений при необходимости

if __name__ == "__main__":
    main()
