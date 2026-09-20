# MediCompare

An AI-assisted web app for understanding medicine information and price differences — built for **First Commit**, part of the AWS × WeMakeDevs Bharat Builds Tour 2026.

> **Informational tool only.** MediCompare does not diagnose, prescribe, or recommend medicines. All prices in this MVP are clearly labelled demo data.

---

## Problem

When someone is handed a prescription, the price they pay can vary a lot between listings of the same medicine and strength. But most comparison tools quietly imply that two products are medically interchangeable in order to sell you something — and that's a clinical claim no comparison tool has any business making. People end up either overpaying, or switching medicines on the word of a website.

## Solution

MediCompare separates the two questions that usually get tangled together:

1. **What do these listings actually cost, and how do they differ?** — that's arithmetic, and the app answers it directly.
2. **Should I take a different one?** — that's clinical, and the app refuses to answer it, redirecting the user to a pharmacist or doctor instead.

An AI assistant, built with the **AWS Strands Agents SDK** and connected to **Amazon Bedrock** (Claude Sonnet 4.6), explains what the user is looking at in plain language — constrained by system prompt to never cross from explanation into prescription.

## Key features

- **Medicine comparison** — search by name and strength, get every option in the demo dataset
- **Price difference calculation** — each option measured against a reference listing
- **Demo savings calculation** — arithmetic difference, presented as arithmetic, not a promise
- **AI assistant** — plain-language explanations of results and terminology
- **Responsive UI** — works on desktop, laptop, tablet and mobile
- **Safety-focused AI responses** — no diagnosis, no prescribing, no equivalence claims
- **Honest AI labelling** — every reply states whether it came from Bedrock or local demo mode

---

## Technology stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5 |
| Backend | Python, Flask, Flask-CORS |
| AI | AWS Strands Agents SDK, Amazon Bedrock |
| Version control | Git, GitHub |

No frontend framework. No database. No authentication. The MVP does not need them.

---

## How we used AWS

We built MediCompare's AI assistant using the **AWS Strands Agents SDK**, an open-source agent framework. Strands handles the agent loop and model binding, letting our Flask backend (`backend/agent.py`) stay a thin, focused layer rather than reimplementing agent orchestration from scratch.

The agent is configured with a strict system prompt: it explains price differences, comparison results, and general medicine terminology in plain language, but is explicitly barred from diagnosing, prescribing, or recommending any medication change — it redirects those questions to a qualified doctor or pharmacist every time.

The Strands agent is wired to use **Amazon Bedrock** (Claude Sonnet 4.6) as its model backend — swapping providers is a one-line config change (`agent.py`, `BedrockModel`) since Strands abstracts the underlying model.
