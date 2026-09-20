"""
app.py
------
The MediCompare Flask backend.

Endpoints
---------
GET  /api/health    Service status and current AI mode.
GET  /api/examples  The medicine/strength pairs present in the demo dataset.
POST /api/compare   Compare demo listings for a medicine and strength.
POST /api/chat      Ask the MediCompare AI assistant a question.

Run with:  python app.py
"""

import logging

from flask import Flask, jsonify, request
from flask_cors import CORS

from data import CURRENCY, available_medicines, find_options
from agent import DISCLAIMER, ai_status, ask_assistant

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

app = Flask(__name__)
CORS(app)  # lets the frontend page call this API from the browser

# Shown with every comparison so the interface can never present demo prices as real.
DEMO_NOTICE = (
    "DEMO DATA — Prices shown are for demonstration only and are not current "
    "market prices."
)


def money(value):
    """Format a demo price for display, e.g. 14.5 -> '₹14.50'."""
    return f"{CURRENCY}{value:,.2f}"


# ---------------------------------------------------------------------------
# GET /api/health
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "MediCompare",
        **ai_status(),
    })


# ---------------------------------------------------------------------------
# GET /api/examples
# ---------------------------------------------------------------------------

@app.get("/api/examples")
def examples():
    """Let the frontend show users what the demo dataset actually contains."""
    return jsonify({
        "success": True,
        "demo_data": True,
        "examples": available_medicines(),
    })


# ---------------------------------------------------------------------------
# POST /api/compare
# ---------------------------------------------------------------------------

@app.post("/api/compare")
def compare():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({
            "success": False,
            "message": "Send a JSON body with a medicine name and strength.",
        }), 400

    medicine = str(payload.get("medicine", "")).strip()
    strength = str(payload.get("strength", "")).strip()

    if not medicine:
        return jsonify({"success": False, "message": "Please enter a medicine name."}), 400
    if not strength:
        return jsonify({"success": False, "message": "Please enter the medicine strength."}), 400
    if len(medicine) > 80 or len(strength) > 40:
        return jsonify({
            "success": False,
            "message": "That input looks too long. Enter a medicine name and a strength "
                       "such as 500mg.",
        }), 400

    try:
        options = find_options(medicine, strength)
    except Exception:
        app.logger.exception("Lookup failed")
        return jsonify({
            "success": False,
            "message": "Something went wrong on the server. Please try again.",
        }), 500

    if not options:
        return jsonify({
            "success": False,
            "message": "Medicine not found in the demo dataset.",
        }), 404

    # The reference listing is the baseline every difference is measured against.
    reference = next((o for o in options if o.get("is_reference")), options[0])
    reference_price = reference["price"]

    # Sort the comparison options from lowest price to highest.
    ordered = sorted(options, key=lambda o: o["price"])

    results = []
    for option in ordered:
        difference = round(reference_price - option["price"], 2)
        results.append({
            "option_name": option["option_name"],
            "price_value": option["price"],
            "price": money(option["price"]),
            "difference_value": difference,
            # Positive difference = lower than the reference listing.
            "price_difference": (
                "Reference listing" if option is reference
                else f"{money(abs(difference))} {'lower' if difference > 0 else 'higher'}"
            ),
            "potential_savings": money(difference) if difference > 0 else "—",
            "is_reference": option is reference,
            "information": option["information"],
        })

    lowest = ordered[0]
    potential_difference = round(reference_price - lowest["price"], 2)

    return jsonify({
        "success": True,
        "demo_data": True,
        "medicine": reference["medicine_name"],
        "strength": reference["strength"],
        "results": results,
        "reference_option": reference["option_name"],
        "reference_price": money(reference_price),
        "comparison_option": lowest["option_name"],
        "comparison_price": money(lowest["price"]),
        "potential_difference": money(potential_difference),
        "notice": DEMO_NOTICE,
        "disclaimer": DISCLAIMER,
    })


# ---------------------------------------------------------------------------
# POST /api/chat
# ---------------------------------------------------------------------------

@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({
            "success": False,
            "message": "Send a JSON body containing your question.",
        }), 400

    message = str(payload.get("message", "")).strip()
    if not message:
        return jsonify({"success": False, "message": "Please type a question."}), 400
    if len(message) > 1000:
        return jsonify({
            "success": False,
            "message": "That question is too long. Try asking it in a sentence or two.",
        }), 400

    context = payload.get("context")
    if not isinstance(context, dict):
        context = None

    try:
        answer = ask_assistant(message, context)
    except Exception:
        app.logger.exception("Assistant failed")
        return jsonify({
            "success": False,
            "message": "The assistant is unavailable right now. Please try again.",
        }), 500

    return jsonify({
        "success": True,
        "reply": answer["reply"],
        "source": answer["source"],
        "note": answer.get("note"),
        "disclaimer": DISCLAIMER,
    })


# ---------------------------------------------------------------------------
# Fallbacks
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(_):
    return jsonify({"success": False, "message": "That endpoint does not exist."}), 404


@app.errorhandler(500)
def server_error(_):
    return jsonify({
        "success": False,
        "message": "Something went wrong on the server. Please try again.",
    }), 500


if __name__ == "__main__":
    status = ai_status()
    print("\nMediCompare backend starting")
    print(f"  AI mode : {status['ai_mode']}")
    if status["ai_mode"] == "bedrock":
        print(f"  Model   : {status['model_id']}  ({status['region']})")
    else:
        print("  Bedrock is off. Set AI_MODE=bedrock to use Amazon Bedrock.")
    print("  API     : http://127.0.0.1:5000/api/health\n")
        import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
