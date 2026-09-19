"""
agent.py
--------
The MediCompare AI assistant.

Two modes are supported:

  AI_MODE=bedrock   Uses the AWS Strands Agents SDK with Amazon Bedrock.
  AI_MODE=mock      Uses local, predefined informational replies so the UI can
                    be demonstrated without an AWS account.

Every reply carries a "source" field ("amazon-bedrock" or "local-mock") so the
interface can state honestly where the answer came from. A mock reply is never
presented as a Bedrock reply.

No credentials are stored in this file. Strands/boto3 read AWS credentials from
the standard places: environment variables, ~/.aws/credentials, or an IAM role.
"""

import os
import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration (all read from environment variables, never hard-coded)
# ---------------------------------------------------------------------------

AI_MODE = os.getenv("AI_MODE", "mock").strip().lower()
BEDROCK_REGION = os.getenv("AWS_REGION", "us-west-2")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "global.anthropic.claude-sonnet-4-6")

SOURCE_BEDROCK = "amazon-bedrock"
SOURCE_MOCK = "local-mock"

DISCLAIMER = (
    "This is informational only and does not replace advice from a doctor or "
    "pharmacist."
)

# ---------------------------------------------------------------------------
# The assistant's instructions
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are MediCompare Assistant, an informational AI assistant \
that helps users understand medicine comparison results, price differences, and \
general terminology.

WHAT YOU DO
- Explain what a price difference between two listed options means.
- Explain the comparison results the user is looking at.
- Explain general medicine-related terminology in simple, beginner-friendly language.
- Help the user understand what they should verify themselves (strength, form,
  composition, pack size, expiry, licensing) before considering another option.
- Suggest specific questions the user can ask their doctor or pharmacist.
- State plainly that the prices in this application are unverified demonstration
  data, not current market prices.

WHAT YOU MUST NEVER DO
- Never diagnose a condition.
- Never prescribe or recommend a medicine.
- Never tell someone to start, stop, switch or change any medication.
- Never claim two medicines are medically equivalent or interchangeable.
- Never invent prices, manufacturers, dosages, clinical facts or medicine information.
  If you do not have the information, say that it needs to be verified.
- Never give personalised medical treatment decisions.

WHEN THE USER ASKS ABOUT CHANGING MEDICATION
Respond with guidance such as: "Please discuss this with a qualified doctor or
pharmacist before making any medication change." Then explain what information
would be useful to bring to that conversation.

STYLE
Keep answers short, clear and plain. Three or four sentences is usually enough.
Use simple words rather than clinical jargon, and explain any term you do use.
"""

# ---------------------------------------------------------------------------
# Mock mode: predefined informational replies
# ---------------------------------------------------------------------------

MOCK_REPLIES = [
    # ORDER MATTERS. The first match wins, so anything that sounds like a request
    # for a medication decision is checked before the general explanation rules.
    (
        ("switch", "should i change", "should i stop", "should i start", "instead of",
         "replace", "is it safe", "can i take", "should i take", "should i buy",
         "which one should", "recommend", "better for me", "suitable for me"),
        "Please discuss this with a qualified doctor or pharmacist before making any "
        "medication change. MediCompare only shows listed price information and cannot "
        "judge whether an option is suitable for you. Bring your current pack or "
        "prescription to that conversation, along with the option you are curious about.",
    ),
    (
        ("price difference", "why is", "cheaper", "expensive", "cost more", "price gap"),
        "A price difference between two listings usually reflects things like the brand, "
        "the pack size, the pharmacy's own pricing and local taxes, rather than anything "
        "about how the medicine works. Two listings that share an active ingredient name "
        "and strength can still differ in pack size or form, so the per-tablet price is "
        "the fairer thing to compare. The figures in this demo are sample values, not "
        "current market prices.",
    ),
    (
        ("verify", "check", "before considering", "what should i look", "confirm"),
        "Before considering any other option, check five things on the physical pack: the "
        "active ingredient name, the strength, the form (tablet, capsule, syrup, "
        "immediate or extended release), the number of units in the pack, and the expiry "
        "date. Also check that it is properly licensed and sold by a registered pharmacy. "
        "A pharmacist can confirm all of this in under a minute.",
    ),
    (
        ("pharmacist", "ask my doctor", "ask the doctor", "questions", "what should i ask"),
        "Useful questions to ask are: is this listing the same active ingredient and "
        "strength as what I take now? Is the form the same? Would anything about my other "
        "medicines or conditions make one option unsuitable? And is there a reason my "
        "prescription specifies a particular product? Take your current pack or "
        "prescription with you so they can see the exact details.",
    ),
    (
        ("generic", "brand", "branded"),
        "In general, a brand name is the marketing name a company gives a product, while "
        "the generic name is the active ingredient itself. Whether two specific listings "
        "are actually interchangeable is a question for a pharmacist, not for a price "
        "comparison tool, so this assistant will not make that claim.",
    ),
    (
        ("savings", "save", "potential difference", "how much"),
        "The savings figure here is simply the arithmetic difference between the reference "
        "listing and the lower-priced listing in the demo dataset. It is a demonstration "
        "calculation, not a promise: real prices vary by pharmacy, pack size and time, and "
        "the right choice for you is a clinical question, not only a price one.",
    ),
    (
        ("strength", "mg", "dosage", "dose"),
        "Strength is the amount of active ingredient in each unit, for example 500mg in one "
        "tablet. It is not the same as the dose, which is how much you take and how often. "
        "A comparison only makes sense between listings of the same strength, and your dose "
        "is something only your prescriber should set or change.",
    ),
    (
        ("demo", "real price", "prices real", "is this real", "accurate", "verified",
         "where do these prices", "sample data"),
        "The prices in this application are demonstration data created for a hackathon "
        "build. They are not sourced from any pharmacy or price database and are not "
        "current market prices. For real pricing, check a licensed pharmacy directly.",
    ),
]

MOCK_DEFAULT = (
    "MediCompare can explain what you are seeing in the comparison table: what a price "
    "difference means, what the terms on the pack mean, and what to verify before you "
    "consider another option. It cannot advise on which medicine is right for you. Try "
    "asking about the price difference, or about what to check with your pharmacist."
)


def mock_reply(message):
    """Return a predefined informational reply based on simple keyword matching."""
    text = (message or "").lower()
    for keywords, reply in MOCK_REPLIES:
        if any(keyword in text for keyword in keywords):
            return reply
    return MOCK_DEFAULT


# ---------------------------------------------------------------------------
# Bedrock mode: Strands Agents SDK
# ---------------------------------------------------------------------------

_agent = None  # created once, on first use


def build_agent():
    """
    Create the Strands agent backed by Amazon Bedrock.

    Imported lazily so that mock mode works even if strands-agents is not
    installed, and so that an AWS misconfiguration does not stop the server
    from starting.
    """
    from strands import Agent
    from strands.models import BedrockModel

    bedrock_model = BedrockModel(
        model_id=BEDROCK_MODEL_ID,
        region_name=BEDROCK_REGION,
        temperature=0.3,
    )

    return Agent(
        model=bedrock_model,
        system_prompt=SYSTEM_PROMPT,
        callback_handler=None,  # no streaming to stdout; we want the final text
    )


def get_agent():
    """Return the shared agent instance, creating it the first time it is needed."""
    global _agent
    if _agent is None:
        _agent = build_agent()
    return _agent


def extract_text(result):
    """Pull the plain text out of a Strands AgentResult."""
    message = getattr(result, "message", None)
    if isinstance(message, dict):
        parts = [
            block["text"]
            for block in message.get("content", [])
            if isinstance(block, dict) and "text" in block
        ]
        if parts:
            return "\n".join(parts).strip()
    return str(result).strip()


# ---------------------------------------------------------------------------
# Public entry point used by app.py
# ---------------------------------------------------------------------------

def build_prompt(message, context):
    """Combine the user's question with the comparison they are looking at."""
    if not context:
        return message

    lines = [
        "The user is currently looking at this demo comparison "
        "(sample data, not verified current prices):",
        f"Medicine: {context.get('medicine', 'unknown')}",
        f"Strength: {context.get('strength', 'unknown')}",
    ]
    for option in context.get("results", [])[:6]:
        lines.append(
            f"- {option.get('option_name')}: {option.get('price')}"
        )
    lines.append("")
    lines.append(f"Their question: {message}")
    return "\n".join(lines)


def ask_assistant(message, context=None):
    """
    Answer a user question.

    Returns a dict: {"reply": str, "source": "amazon-bedrock" | "local-mock"}
    Falls back to mock mode if Bedrock is unavailable, and says so honestly.
    """
    message = (message or "").strip()
    if not message:
        return {
            "reply": "Type a question about your comparison results to get started.",
            "source": SOURCE_MOCK,
        }

    if AI_MODE != "bedrock":
        return {"reply": mock_reply(message), "source": SOURCE_MOCK}

    try:
        agent = get_agent()
        result = agent(build_prompt(message, context))
        reply = extract_text(result)
        if not reply:
            raise ValueError("Empty response from the model")
        return {"reply": reply, "source": SOURCE_BEDROCK}
    except Exception:
        # Log the real error for the developer, show the user a safe message.
        logger.exception("Bedrock request failed; falling back to local mock reply")
        return {
            "reply": mock_reply(message),
            "source": SOURCE_MOCK,
            "note": "Amazon Bedrock is not reachable right now, so this is a local "
                    "demo reply.",
        }


def ai_status():
    """Describe the current AI configuration for the /api/health endpoint."""
    return {
        "ai_mode": "bedrock" if AI_MODE == "bedrock" else "mock",
        "model_id": BEDROCK_MODEL_ID if AI_MODE == "bedrock" else None,
        "region": BEDROCK_REGION if AI_MODE == "bedrock" else None,
    }