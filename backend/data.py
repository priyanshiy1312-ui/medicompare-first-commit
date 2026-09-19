"""
data.py
-------
DEMO DATA for MediCompare.

IMPORTANT
=========
Everything in this file is SAMPLE DATA created for a hackathon demonstration.
The prices are NOT real, NOT current, and NOT sourced from any pharmacy,
manufacturer or price database. They exist only so the user interface has
something to display.

The dataset also deliberately avoids words like "equivalent", "substitute"
or "better". Each entry is called a "comparison option" instead, because
MediCompare does not make medical claims.
"""

# Currency symbol used when showing demo prices in the interface.
CURRENCY = "₹"

# Each record is one comparison option for one medicine + strength.
#   medicine_name -> the generic / searched name
#   strength      -> the strength the option is listed under
#   option_name   -> the label shown in the comparison table
#   price         -> DEMO price only
#   is_reference  -> the option used as the baseline for price differences
#   information   -> general, non-prescriptive information text
DEMO_MEDICINES = [
    # ---------------- Paracetamol 500mg ----------------
    {
        "medicine_name": "Paracetamol",
        "strength": "500mg",
        "option_name": "Demo Option A (branded listing)",
        "price": 32.00,
        "is_reference": True,
        "information": "Paracetamol is commonly used to reduce fever and relieve mild pain. "
                       "Dosage limits matter; confirm the correct dose with a pharmacist.",
    },
    {
        "medicine_name": "Paracetamol",
        "strength": "500mg",
        "option_name": "Demo Option B (generic listing)",
        "price": 14.50,
        "is_reference": False,
        "information": "Listed under the same active ingredient name and strength in this demo "
                       "dataset. Composition and licensing must be verified with a pharmacist.",
    },
    {
        "medicine_name": "Paracetamol",
        "strength": "500mg",
        "option_name": "Demo Option C (generic listing)",
        "price": 18.75,
        "is_reference": False,
        "information": "A second generic listing in the demo dataset, shown to illustrate that "
                       "listed prices can vary between options.",
    },
    {
        "medicine_name": "Paracetamol",
        "strength": "500mg",
        "option_name": "Demo Option D (store listing)",
        "price": 21.00,
        "is_reference": False,
        "information": "Included to show how a comparison table sorts multiple options. "
                       "Not a recommendation of any kind.",
    },

    # ---------------- Ibuprofen 400mg ----------------
    {
        "medicine_name": "Ibuprofen",
        "strength": "400mg",
        "option_name": "Demo Option A (branded listing)",
        "price": 48.00,
        "is_reference": True,
        "information": "Ibuprofen is an anti-inflammatory pain reliever. It is not suitable for "
                       "everyone; a doctor or pharmacist can advise on suitability.",
    },
    {
        "medicine_name": "Ibuprofen",
        "strength": "400mg",
        "option_name": "Demo Option B (generic listing)",
        "price": 22.00,
        "is_reference": False,
        "information": "Generic listing in the demo dataset under the same active ingredient "
                       "name and strength.",
    },
    {
        "medicine_name": "Ibuprofen",
        "strength": "400mg",
        "option_name": "Demo Option C (generic listing)",
        "price": 29.50,
        "is_reference": False,
        "information": "A second generic listing included for demonstration of price spread.",
    },

    # ---------------- Cetirizine 10mg ----------------
    {
        "medicine_name": "Cetirizine",
        "strength": "10mg",
        "option_name": "Demo Option A (branded listing)",
        "price": 55.00,
        "is_reference": True,
        "information": "Cetirizine is an antihistamine often used for allergy symptoms. "
                       "Some people experience drowsiness.",
    },
    {
        "medicine_name": "Cetirizine",
        "strength": "10mg",
        "option_name": "Demo Option B (generic listing)",
        "price": 19.00,
        "is_reference": False,
        "information": "Generic listing in the demo dataset. Verify the actual composition on "
                       "the physical pack before buying anything.",
    },
    {
        "medicine_name": "Cetirizine",
        "strength": "10mg",
        "option_name": "Demo Option C (store listing)",
        "price": 27.25,
        "is_reference": False,
        "information": "Demo listing included to show a mid-range price point.",
    },

    # ---------------- Metformin 500mg ----------------
    {
        "medicine_name": "Metformin",
        "strength": "500mg",
        "option_name": "Demo Option A (branded listing)",
        "price": 96.00,
        "is_reference": True,
        "information": "Metformin is a long-term prescription medicine. Any change to a "
                       "long-term medicine must be discussed with the prescribing doctor.",
    },
    {
        "medicine_name": "Metformin",
        "strength": "500mg",
        "option_name": "Demo Option B (generic listing)",
        "price": 41.00,
        "is_reference": False,
        "information": "Generic listing in the demo dataset. Release profile (for example "
                       "immediate vs extended release) is a detail a pharmacist should confirm.",
    },
    {
        "medicine_name": "Metformin",
        "strength": "500mg",
        "option_name": "Demo Option C (generic listing)",
        "price": 58.50,
        "is_reference": False,
        "information": "A second generic listing shown for comparison purposes only.",
    },

    # ---------------- Omeprazole 20mg ----------------
    {
        "medicine_name": "Omeprazole",
        "strength": "20mg",
        "option_name": "Demo Option A (branded listing)",
        "price": 88.00,
        "is_reference": True,
        "information": "Omeprazole reduces stomach acid production. Length of use is something "
                       "a doctor decides, not a comparison tool.",
    },
    {
        "medicine_name": "Omeprazole",
        "strength": "20mg",
        "option_name": "Demo Option B (generic listing)",
        "price": 34.00,
        "is_reference": False,
        "information": "Generic listing in the demo dataset under the same strength.",
    },
    {
        "medicine_name": "Omeprazole",
        "strength": "20mg",
        "option_name": "Demo Option C (store listing)",
        "price": 46.75,
        "is_reference": False,
        "information": "Demo listing included to illustrate sorting by price.",
    },

    # ---------------- Amoxicillin 250mg ----------------
    {
        "medicine_name": "Amoxicillin",
        "strength": "250mg",
        "option_name": "Demo Option A (branded listing)",
        "price": 112.00,
        "is_reference": True,
        "information": "Amoxicillin is an antibiotic. Antibiotic courses are prescribed and "
                       "should be completed exactly as directed by a doctor.",
    },
    {
        "medicine_name": "Amoxicillin",
        "strength": "250mg",
        "option_name": "Demo Option B (generic listing)",
        "price": 63.00,
        "is_reference": False,
        "information": "Generic listing in the demo dataset under the same strength.",
    },
    {
        "medicine_name": "Amoxicillin",
        "strength": "250mg",
        "option_name": "Demo Option C (generic listing)",
        "price": 79.00,
        "is_reference": False,
        "information": "A second demo listing shown for comparison purposes only.",
    },

    # ---------------- Azithromycin 500mg ----------------
    {
        "medicine_name": "Azithromycin",
        "strength": "500mg",
        "option_name": "Demo Option A (branded listing)",
        "price": 138.00,
        "is_reference": True,
        "information": "Azithromycin is a prescription antibiotic. A pharmacist can explain "
                       "how a listed pack size affects the total price.",
    },
    {
        "medicine_name": "Azithromycin",
        "strength": "500mg",
        "option_name": "Demo Option B (generic listing)",
        "price": 74.50,
        "is_reference": False,
        "information": "Generic listing in the demo dataset under the same strength.",
    },
    {
        "medicine_name": "Azithromycin",
        "strength": "500mg",
        "option_name": "Demo Option C (store listing)",
        "price": 99.00,
        "is_reference": False,
        "information": "Demo listing included to show a third price point.",
    },
]


def normalise(text):
    """Lowercase and strip a value so that search is forgiving of spacing and case."""
    return (text or "").strip().lower().replace(" ", "")


def find_options(medicine, strength):
    """
    Return every demo comparison option matching the medicine name and strength.

    Matching is case-insensitive and ignores spaces, so "500 MG" finds "500mg".
    Returns an empty list when nothing matches.
    """
    wanted_medicine = normalise(medicine)
    wanted_strength = normalise(strength)

    return [
        option
        for option in DEMO_MEDICINES
        if normalise(option["medicine_name"]) == wanted_medicine
        and normalise(option["strength"]) == wanted_strength
    ]


def available_medicines():
    """Return the list of medicine/strength pairs present in the demo dataset."""
    seen = []
    for option in DEMO_MEDICINES:
        pair = {"medicine": option["medicine_name"], "strength": option["strength"]}
        if pair not in seen:
            seen.append(pair)
    return seen