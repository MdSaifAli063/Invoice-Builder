# 🧾 Invoice Builder (Flask)

A tiny, zero‑database invoice builder with a clean UI. Edit company/client info, add line items, and print a polished invoice — all in your browser.

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?logo=dependabot)](#)
[![License](https://img.shields.io/badge/License-Choose%20one-informational)](#-license)

---

## ✨ Features

- 📝 Edit Company, Client, and Invoice metadata
- ➕➖ Add/Remove line items with quantity and unit price
- 🧮 Auto-calculated Subtotal, Tax, Shipping, Total, and Balance Due
- 🖨️ Printer-friendly invoice page (with optional auto-print)
- 🌓 Light/Dark theme toggle (persisted in localStorage)
- 🧪 Test route to verify prints/logging: `/_test_print`
- 🪵 Immediate stdout prints (auto-flushed) + structured logging

All data is in-memory for simplicity (resets on restart).

---
## 🖼️ Preview
- Setup
![image](https://github.com/MdSaifAli063/Invoice-Builder/blob/ab7662e6134d92bd8ba35699b55182cc78efef49/Screenshot%202025-09-28%20014932.png)
![image](https://github.com/MdSaifAli063/Invoice-Builder/blob/238d832cc1c960989c85df9d95b3da47a2195522/Screenshot%202025-09-28%20015029.png)



## 🚀 Quickstart

1) Create a virtual environment and install dependencies
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install flask


Run the app
python app.py



Open in your browser
Setup UI: http://localhost:5000/setup
Invoice view: http://localhost:5000/invoice
Verify print/log output (optional)
curl http://localhost:5000/_test_print


You should see both a print() line and a structured INFO log in your terminal.

🧭 App Structure
app.py                 # Flask application, routes, in-memory data, logging
templates/
  setup.html           # Configure company/client/invoice and manage items
  invoice.html         # Pretty, printable invoice view
static/ (optional)
  css/app.css          # Extract inline CSS here if desired


Note: Ensure your HTML templates live in a "templates" directory next to app.py.

🔌 Endpoints
GET / → redirects to /setup
GET /setup → setup page (forms for company, client, invoice meta, items table)
GET /invoice → printable invoice page (supports ?print=1 to auto-open print dialog)
Mutating endpoints (form POSTs):

POST /add_item
Fields: quantity (int), description (str), unit_price (float)
POST /remove_item
Fields: description (str, exact match)
POST /update_company
Fields: name, address, phone, email, website, logo_url
POST /update_client
Fields: name, address, phone, email
POST /update_meta
Fields: invoice_number, invoice_date, due_date, currency_symbol, tax_rate, shipping, amount_paid, notes
POST /clear_all → resets everything to defaults
Utility:

GET /_test_print → emits both print() and logger output
🧪 cURL Examples
Add an item:

curl -X POST http://localhost:5000/add_item \
  -d "quantity=2" \
  -d "description=Design work" \
  -d "unit_price=125.50"



Remove an item by description:

curl -X POST http://localhost:5000/remove_item \
  -d "description=Design work"



Update meta:

curl -X POST http://localhost:5000/update_meta \
  -d "invoice_number=0002" \
  -d "invoice_date=2025-01-01" \
  -d "due_date=2025-01-31" \
  -d "currency_symbol=$" \
  -d "tax_rate=5" \
  -d "shipping=10" \
  -d "amount_paid=0" \
  -d "notes=Payable within 30 days."


🖨️ Printing
Open /invoice and use your browser’s Print dialog.
To auto-open print, visit /invoice?print=1.
Tip: Use the browser’s “Save as PDF” to export.
📜 Logging and Visibility
All print() calls are auto-flushed to stdout, so you’ll see them immediately.
Structured logs stream to stdout; every request is logged before and after handling.
Avoid duplicate logs in debug mode:

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)



🛠️ Customizing the UI
Tweak templates/setup.html and templates/invoice.html to match your brand.
Extract inline CSS into static/css/app.css and include:
<link rel="stylesheet" href="{{ url_for('static', filename='css/app.css') }}">


Keep headings/labels clear for printability and accessibility.
🧯 Troubleshooting
I don’t see print output
Use /_test_print to verify terminal logs.
Ensure you’re watching the server process logs (stdout).
In containers/process managers, stdout may be redirected — check service logs.
Totals look wrong
Ensure quantity and unit_price are numeric. The app clamps tax_rate to 0–100 and defaults empty inputs.
🤝 Contributing
Fork the repo, create a feature branch, and open a PR.
For UI tweaks, include before/after screenshots.
📄 License
No license specified. Choose a license (e.g., MIT, Apache-2.0) and add a LICENSE file to clarify usage.

Made with ❤️ using Flask.
