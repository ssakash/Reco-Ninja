import tkinter as tk
from tkinter import ttk, messagebox
from reconinja import reconinja

def run_recon():
    """Run the Reco-Ninja script with user input."""
    url = url_entry.get()
    api_key = api_key_entry.get()

    if not url:
        messagebox.showerror("Input Error", "Please provide URL.")
        return

    try:
        result = reconinja(url,0).robotsanalysis()
        output_text.insert("1.0", result)
    except Exception as e:
        messagebox.showerror("Execution Error", str(e))

# Initialize the GUI
root = tk.Tk()
root.title("Reco-Ninja GUI")

# URL Input
url_label = tk.Label(root, text="Target URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# API Key Input
api_key_label = tk.Label(root, text="API Key:")
api_key_label.pack(pady=5)
api_key_entry = tk.Entry(root, width=50, show="*")
api_key_entry.pack(pady=5)

# Run Button
run_button = tk.Button(root, text="Run Reco-Ninja", command=run_recon)
run_button.pack(pady=10)

# Output Display
output_label = tk.Label(root, text="Output:")
output_label.pack(pady=5)
output_text = tk.Text(root, width=60, height=20)
output_text.pack(pady=10)

# Start the GUI event loop
root.mainloop()
