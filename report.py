from fpdf import FPDF
import re
import chardet
import unicodedata

def detect_encoding(file_path):
    """Detects the encoding of a file."""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    return chardet.detect(raw_data)['encoding']

def clean_text(text):
    """Cleans broken encoding artifacts from text."""
    text = text.encode('utf-8', 'ignore').decode('utf-8')
    return unicodedata.normalize('NFKD', text)

def remove_ansi_codes(text):
    """Removes ANSI color codes from text."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def parse_httpx_output(file_path):
    """Parses the httpx output and extracts URLs and status codes, excluding status 400, and sorts them."""
    urls = []
    pattern = re.compile(r'(https?://\S+) \[(\d{3})\]')
    
    encoding = detect_encoding(file_path)
    print(f"Detected encoding: {encoding}")
    
    with open(file_path, 'r', encoding=encoding, errors='replace') as file:
        for line in file:
            line = remove_ansi_codes(clean_text(line.strip()))
            match = pattern.search(line)
            if match:
                url, status = match.groups()
                if status != "400":
                    urls.append((url, int(status)))
    
    urls.sort(key=lambda x: x[1])  # Sort by status code
    print(f"Parsed and sorted URLs: {urls}")
    return urls

def generate_pdf(output_pdf, urls):
    """Generates a structured PDF with URLs sorted by status code, excluding status 400."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Filtered URLs Report", ln=True, align='C')
    pdf.ln(10)
    
    if not urls:
        pdf.cell(200, 8, "No URLs found.", ln=True)
    else:
        for url, status in urls:
            pdf.multi_cell(0, 6, f"{url} - [{status}]")
            pdf.ln(2)
    
    pdf.output(output_pdf, 'F')
    print(f"[+] PDF Report saved as {output_pdf}")

# Example Usage
file_path = "endpoints.txt"  # Replace with your actual file
output_pdf = "urls_Report.pdf"
urls = parse_httpx_output(file_path)
generate_pdf(output_pdf, urls)
