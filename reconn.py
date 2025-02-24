import subprocess
import report
import sys

# Step 1: Run AssetFinder and save output to result.txt
input_file = "scope.txt"  # Change this to your actual input file name
output_file = "result.txt"

print("[+] Running AssetFinder...")
with open(output_file, "w") as outfile:
    subprocess.run(["assetfinder"], stdin=open(input_file, "r"), stdout=outfile, text=True)

# Step 2: Run httpx on the result from AssetFinder
httpx_output_file = "httpx_result.txt"
print("[+] Running httpx on result.txt...")
with open(httpx_output_file, "w") as outfile:
    subprocess.run(["httpx", "-server", "-sc", "-title"], stdin=open(output_file, "r"), stdout=outfile, text=True)

print(f"[+] Done! Results saved to {httpx_output_file}")
output_pdf = f"{sys.argv[1]}.pdf"
urls = report.parse_httpx_output(httpx_output_file)
report.generate_pdf(output_pdf, urls)