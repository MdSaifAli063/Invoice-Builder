from datetime import date
from flask import Flask, render_template, request, redirect, url_for
import logging
import sys
import builtins

# Ensure all print() calls flush immediately to the console
_builtin_print = builtins.print
def print(*args, **kwargs):
    kwargs.setdefault("flush", True)
    return _builtin_print(*args, **kwargs)

# Improve stdout behavior (Python 3.7+) to line-buffered if available
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

app = Flask(__name__)

# Configure logging to stdout so logs are visible in terminal or container logs
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
app.logger.setLevel(logging.DEBUG)

# Optional: log each request/response for visibility
@app.before_request
def _log_request():
    app.logger.debug("-> %s %s", request.method, request.path)

@app.after_request
def _log_response(response):
    app.logger.debug("<- %s %s %s", request.method, request.path, response.status_code)
    return response


# In-memory data stores (for demo; resets on restart)
invoice_items = []

company = {
    "name": "Your Company Name",
    "address": "",
    "phone": "",
    "email": "",
    "website": "",
    "logo_url": "",
}

client = {
    "name": "Client Name",
    "address": "",
    "phone": "",
    "email": "",
}

meta = {
    "invoice_number": "0001",
    "invoice_date": date.today().isoformat(),
    "due_date": "",
    "currency_symbol": "$",
    "tax_rate": 3.0,       # percent
    "shipping": 0.0,
    "amount_paid": 0.0,
    "notes": "Thank you for your business!",
}


def _parse_float(val, default=0.0):
    try:
        if val is None or str(val).strip() == "":
            return default
        return float(val)
    except ValueError:
        return default


def compute_totals():
    subtotal = sum(item["quantity"] * item["unit_price"] for item in invoice_items)
    tax_rate = _parse_float(meta.get("tax_rate", 3.0), 3.0)
    tax = subtotal * (tax_rate / 100.0)
    shipping = _parse_float(meta.get("shipping", 0.0), 0.0)
    total = subtotal + tax + shipping
    return subtotal, tax, shipping, total


@app.route("/")
def index():
    return redirect(url_for("setup"))


@app.route("/setup")
def setup():
    subtotal, tax, shipping, total = compute_totals()
    return render_template(
        "setup.html",
        company=company,
        client=client,
        items=invoice_items,
        invoice_number=meta.get("invoice_number"),
        invoice_date=meta.get("invoice_date"),
        due_date=meta.get("due_date"),
        currency_symbol=meta.get("currency_symbol", "$"),
        tax_rate=meta.get("tax_rate", 3.0),
        shipping=shipping,
        subtotal=subtotal,
        tax=tax,
        total=total,
        amount_paid=meta.get("amount_paid", 0.0),
        notes=meta.get("notes"),
    )


@app.route("/invoice")
def invoice():
    subtotal, tax, shipping, total = compute_totals()
    return render_template(
        "invoice.html",
        company=company,
        client=client,
        items=invoice_items,
        invoice_number=meta.get("invoice_number"),
        invoice_date=meta.get("invoice_date"),
        due_date=meta.get("due_date"),
        currency_symbol=meta.get("currency_symbol", "$"),
        tax_rate=meta.get("tax_rate", 3.0),
        shipping=shipping,
        subtotal=subtotal,
        tax=tax,
        total=total,
        amount_paid=meta.get("amount_paid", 0.0),
        notes=meta.get("notes"),
    )


@app.route("/add_item", methods=["POST"])
def add_item():
    quantity = int(request.form.get("quantity", 1))
    description = (request.form.get("description") or "").strip()
    unit_price = _parse_float(request.form.get("unit_price"), 0.0)
    if description:
        invoice_items.append(
            {"quantity": quantity, "description": description, "unit_price": unit_price}
        )
        # Example print to verify output
        print(f"Added item: {description}, qty={quantity}, price={unit_price}")
        app.logger.info("Added item: %s (qty=%s, price=%s)", description, quantity, unit_price)
    return redirect(url_for("setup"))


@app.route("/remove_item", methods=["POST"])
def remove_item():
    description_to_remove = (request.form.get("description") or "").strip()
    if description_to_remove:
        global invoice_items
        before_count = len(invoice_items)
        invoice_items = [
            item for item in invoice_items if item["description"] != description_to_remove
        ]
        after_count = len(invoice_items)
        print(f"Removed item: {description_to_remove} (before={before_count}, after={after_count})")
        app.logger.info(
            "Removed item: %s (before=%s, after=%s)",
            description_to_remove, before_count, after_count
        )
    return redirect(url_for("setup"))


@app.route("/update_company", methods=["POST"])
def update_company():
    company["name"] = (request.form.get("name") or "").strip()
    company["address"] = (request.form.get("address") or "").strip()
    company["phone"] = (request.form.get("phone") or "").strip()
    company["email"] = (request.form.get("email") or "").strip()
    company["website"] = (request.form.get("website") or "").strip()
    company["logo_url"] = (request.form.get("logo_url") or "").strip()
    print("Company updated:", company["name"])
    return redirect(url_for("setup"))


@app.route("/update_client", methods=["POST"])
def update_client():
    client["name"] = (request.form.get("name") or "").strip()
    client["address"] = (request.form.get("address") or "").strip()
    client["phone"] = (request.form.get("phone") or "").strip()
    client["email"] = (request.form.get("email") or "").strip()
    print("Client updated:", client["name"])
    return redirect(url_for("setup"))


@app.route("/update_meta", methods=["POST"])
def update_meta():
    meta["invoice_number"] = (request.form.get("invoice_number") or "").strip() or meta.get("invoice_number")
    meta["invoice_date"] = (request.form.get("invoice_date") or "").strip() or meta.get("invoice_date")
    meta["due_date"] = (request.form.get("due_date") or "").strip()
    meta["currency_symbol"] = (request.form.get("currency_symbol") or "").strip() or "$"
    meta["tax_rate"] = _parse_float(request.form.get("tax_rate"), meta.get("tax_rate", 3.0))
    meta["tax_rate"] = max(0.0, min(100.0, meta["tax_rate"]))  # clamp 0..100
    meta["shipping"] = _parse_float(request.form.get("shipping"), 0.0)
    meta["amount_paid"] = _parse_float(request.form.get("amount_paid"), 0.0)
    meta["notes"] = (request.form.get("notes") or "").strip()
    print("Meta updated:", meta)
    return redirect(url_for("setup"))


@app.route("/clear_all", methods=["POST"])
def clear_all():
    invoice_items.clear()
    for k in list(company.keys()):
        company[k] = "" if k != "name" else "Your Company Name"
    for k in list(client.keys()):
        client[k] = "" if k != "name" else "Client Name"
    meta.update({
        "invoice_number": "0001",
        "invoice_date": date.today().isoformat(),
        "due_date": "",
        "currency_symbol": "$",
        "tax_rate": 3.0,
        "shipping": 0.0,
        "amount_paid": 0.0,
        "notes": "Thank you for your business!",
    })
    print("All data cleared and reset to defaults.")
    return redirect(url_for("setup"))


# Optional test route to verify print/logging quickly
@app.route("/_test_print")
def _test_print():
    print("Test print from /_test_print")
    app.logger.info("Test logger from /_test_print")
    return "OK"


if __name__ == "__main__":
    # If you see duplicate logs, you can set use_reloader=False below.
    app.run(debug=True)