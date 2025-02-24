import requests
import socket
import whois
import dns.resolver
import shodan
from fpdf import FPDF

# Replace with your Shodan API key if using port scanning
SHODAN_API_KEY = "yMO4EXLx0y16ps7hbu6g4qtEbRfDQlJq"

def get_http_headers(url):
    """Retrieve HTTP headers of a given URL."""
    try:
        response = requests.get(url, timeout=5)
        return dict(response.headers)
    except requests.RequestException as e:
        return {"Error": f"Error fetching headers: {e}"}

def get_dns_records(domain):
    """Retrieve DNS records (A, MX, NS, TXT)."""
    records = {}
    try:
        records['A'] = [str(ip) for ip in dns.resolver.resolve(domain, 'A')]
        records['MX'] = [str(mx) for mx in dns.resolver.resolve(domain, 'MX')]
        records['NS'] = [str(ns) for ns in dns.resolver.resolve(domain, 'NS')]
        records['TXT'] = [str(txt) for txt in dns.resolver.resolve(domain, 'TXT')]
    except Exception as e:
        records['Error'] = f"DNS Lookup Failed: {e}"
    return records

def get_whois_info(domain):
    """Retrieve WHOIS information of a domain."""
    try:
        return whois.whois(domain)
    except Exception as e:
        return {"Error": f"Whois lookup failed: {e}"}

def get_subdomains(domain):
    """Fetch potential subdomains using a common wordlist."""
    subdomains = ["www", "mail", "blog", "dev", "test", "shop", "api", "secure"]
    found_subdomains = []
    for sub in subdomains:
        subdomain = f"{sub}.{domain}"
        try:
            socket.gethostbyname(subdomain)
            found_subdomains.append(subdomain)
        except socket.gaierror:
            pass
    return found_subdomains

def get_open_ports(ip):
    """Retrieve open ports using Shodan."""
    try:
        shodan_api = shodan.Shodan(SHODAN_API_KEY)
        result = shodan_api.host(ip)
        return result.get('ports', [])
    except Exception as e:
        return {"Error": f"Shodan lookup failed: {e}"}

def generate_pdf(domain, headers, dns_records, whois_info, subdomains, open_ports):
    """Generate a PDF report with reconnaissance results."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, f"Reconnaissance Report: {domain}", ln=True, align='C')
    pdf.ln(10)

    sections = {
        "HTTP Headers": headers,
        "DNS Records": dns_records,
        "WHOIS Information": whois_info,
        "Subdomains": subdomains,
        "Open Ports": open_ports
    }

    for title, content in sections.items():
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(200, 8, title, ln=True)
        pdf.set_font("Arial", size=10)
        if isinstance(content, dict):
            for key, value in content.items():
                pdf.multi_cell(0, 6, f"{key}: {value}")
        elif isinstance(content, list):
            for item in content:
                pdf.multi_cell(0, 6, str(item))
        else:
            pdf.multi_cell(0, 6, str(content))
        pdf.ln(5)
    
    pdf.output(f"{domain}_recon.pdf")
    print(f"[+] PDF Report saved as {domain}_recon.pdf")

def main(url):
    """Main function to perform reconnaissance."""
    if url.startswith("http"):
        domain = url.split("//")[-1].split("/")[0]
    else:
        domain = url

    print(f"Performing reconnaissance on: {domain}\n")
    
    headers = get_http_headers(url)
    dns_records = get_dns_records(domain)
    whois_info = get_whois_info(domain)
    subdomains = get_subdomains(domain)
    
    try:
        ip = socket.gethostbyname(domain)
        open_ports = get_open_ports(ip)
    except socket.gaierror:
        open_ports = "Unable to resolve IP for domain."
    
    generate_pdf(domain, headers, dns_records, whois_info, subdomains, open_ports)

if __name__ == "__main__":
    target_url = input("Enter the target URL: ")
    main(target_url)
