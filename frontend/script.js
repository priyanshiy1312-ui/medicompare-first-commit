/* ==========================================================================
   MediCompare — script.js
   Talks to the Flask backend. No AWS keys or secrets live here; the browser
   only ever calls our own API.
   ========================================================================== */

const API_BASE = "http://127.0.0.1:5000";

// Remembers the last successful comparison so the AI assistant has context.
let lastComparison = null;

/* ---------------------------- helpers ---------------------------------- */

function el(id) {
  return document.getElementById(id);
}

/** Show a message in the comparison area. type: "danger" | "warning" | "info" */
function showCompareMessage(text, type) {
  const box = el("compareMessage");
  box.className = `alert alert-${type} mt-4`;
  box.textContent = text;
}

function hideCompareMessage() {
  el("compareMessage").className = "alert mt-4 d-none";
}

/** Toggle the loading state of a button that has a spinner inside it. */
function setLoading(button, spinner, label, isLoading, busyText, idleText) {
  button.disabled = isLoading;
  spinner.classList.toggle("d-none", !isLoading);
  label.textContent = isLoading ? busyText : idleText;
}

/** Turn a fetch failure into wording a user can act on. */
function networkMessage() {
  return "Backend is not available. Please make sure the Flask server is running " +
         "at " + API_BASE + ".";
}

/* ------------------------- backend status ------------------------------ */

async function checkBackend() {
  const chip = el("backendStatus");
  const text = el("backendStatusText");
  try {
    const response = await fetch(`${API_BASE}/api/health`);
    const data = await response.json();
    chip.classList.add("is-online");
    text.textContent = data.ai_mode === "bedrock"
      ? "Backend online · Bedrock"
      : "Backend online · demo AI";
  } catch (error) {
    chip.classList.add("is-offline");
    text.textContent = "Backend offline";
  }
}

/* --------------------- demo dataset examples --------------------------- */

async function loadExamples() {
  const container = el("exampleList");
  try {
    const response = await fetch(`${API_BASE}/api/examples`);
    const data = await response.json();

    container.innerHTML = "";
    data.examples.forEach(function (item) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "chip";
      button.textContent = `${item.medicine} ${item.strength}`;
      button.addEventListener("click", function () {
        el("medicineInput").value = item.medicine;
        el("strengthInput").value = item.strength;
        el("compareForm").requestSubmit();
      });
      container.appendChild(button);
    });
  } catch (error) {
    container.innerHTML =
      '<span class="small text-muted">Start the Flask server to load examples.</span>';
  }
}

/* --------------------------- comparison -------------------------------- */

async function handleCompare(event) {
  event.preventDefault();
  hideCompareMessage();

  const medicine = el("medicineInput").value.trim();
  const strength = el("strengthInput").value.trim();

  // Validate in the browser first so obvious mistakes never hit the network.
  if (!medicine) {
    showCompareMessage("Please enter a medicine name.", "warning");
    el("medicineInput").focus();
    return;
  }
  if (!strength) {
    showCompareMessage("Please enter the medicine strength.", "warning");
    el("strengthInput").focus();
    return;
  }

  setLoading(el("compareButton"), el("compareSpinner"), el("compareButtonText"),
             true, "Comparing…", "Compare medicine");

  try {
    const response = await fetch(`${API_BASE}/api/compare`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ medicine: medicine, strength: strength }),
    });

    const data = await response.json();

    if (!response.ok || !data.success) {
      el("results").classList.add("d-none");
      showCompareMessage(data.message || "That comparison could not be completed.",
                         response.status === 404 ? "info" : "warning");
      return;
    }

    lastComparison = data;
    renderResults(data);
    el("results").scrollIntoView({ behavior: "smooth", block: "start" });

  } catch (error) {
    el("results").classList.add("d-none");
    showCompareMessage(networkMessage(), "danger");
  } finally {
    setLoading(el("compareButton"), el("compareSpinner"), el("compareButtonText"),
               false, "Comparing…", "Compare medicine");
  }
}

function renderResults(data) {
  el("resultTitle").textContent = `${data.medicine} ${data.strength}`;
  el("resultSubtitle").textContent = "Demo comparison data";
  el("resultNotice").textContent = data.notice;

  el("referencePrice").textContent = data.reference_price;
  el("referenceOption").textContent = data.reference_option;
  el("comparisonPrice").textContent = data.comparison_price;
  el("comparisonOption").textContent = data.comparison_option;
  el("potentialDifference").textContent = data.potential_difference;

  // Comparison table, already sorted lowest price first by the backend.
  const body = el("resultsBody");
  body.innerHTML = "";

  data.results.forEach(function (option, index) {
    const row = document.createElement("tr");
    if (index === 0 && !option.is_reference) {
      row.className = "is-lowest";
    }

    const nameCell = document.createElement("td");
    nameCell.className = "option-name";
    nameCell.textContent = option.option_name;
    if (option.is_reference) {
      const tag = document.createElement("span");
      tag.className = "option-tag";
      tag.textContent = "Reference";
      nameCell.appendChild(tag);
    }

    const priceCell = document.createElement("td");
    priceCell.textContent = option.price;

    const diffCell = document.createElement("td");
    diffCell.textContent = option.price_difference;

    const savingCell = document.createElement("td");
    savingCell.textContent = option.potential_savings;

    row.append(nameCell, priceCell, diffCell, savingCell);
    body.appendChild(row);
  });

  // General information cards, one per option.
  const info = el("infoCards");
  info.innerHTML = "";
  data.results.forEach(function (option) {
    const col = document.createElement("div");
    col.className = "col-md-6 col-lg-4";

    const card = document.createElement("div");
    card.className = "info-card";

    const heading = document.createElement("h4");
    heading.textContent = option.option_name;

    const text = document.createElement("p");
    text.textContent = option.information;

    card.append(heading, text);
    col.appendChild(card);
    info.appendChild(col);
  });

  el("results").classList.remove("d-none");
}

/* ------------------------- AI assistant -------------------------------- */

function addChatMessage(role, text, source) {
  const log = el("chatLog");

  const wrapper = document.createElement("div");
  wrapper.className = role === "user" ? "chat-msg chat-msg-user" : "chat-msg chat-msg-ai";

  const label = document.createElement("span");
  label.className = "chat-role";
  label.textContent = role === "user" ? "You" : "Assistant";

  const paragraph = document.createElement("p");
  paragraph.textContent = text;

  wrapper.append(label, paragraph);

  // Say honestly where the answer came from.
  if (source) {
    const note = document.createElement("span");
    note.className = "chat-source";
    note.textContent = source === "amazon-bedrock"
      ? "Generated by Amazon Bedrock via AWS Strands Agents"
      : "Local demo response — Amazon Bedrock is not in use";
    wrapper.appendChild(note);
  }

  log.appendChild(wrapper);
  log.scrollTop = log.scrollHeight;
  return wrapper;
}

function addTypingIndicator() {
  const log = el("chatLog");
  const wrapper = document.createElement("div");
  wrapper.className = "chat-msg chat-msg-ai chat-typing";
  wrapper.innerHTML = '<span class="chat-role">Assistant</span><p>Thinking</p>';
  log.appendChild(wrapper);
  log.scrollTop = log.scrollHeight;
  return wrapper;
}

async function handleChat(event) {
  event.preventDefault();

  const input = el("chatInput");
  const message = input.value.trim();
  const errorBox = el("chatMessage");
  errorBox.classList.add("d-none");

  if (!message) {
    errorBox.textContent = "Please type a question.";
    errorBox.classList.remove("d-none");
    input.focus();
    return;
  }

  addChatMessage("user", message);
  input.value = "";

  const typing = addTypingIndicator();
  setLoading(el("chatButton"), el("chatSpinner"), el("chatButtonText"),
             true, "Asking…", "Ask AI");

  try {
    // Send the current comparison along so answers can reference what's on screen.
    const context = lastComparison ? {
      medicine: lastComparison.medicine,
      strength: lastComparison.strength,
      results: lastComparison.results.map(function (option) {
        return { option_name: option.option_name, price: option.price };
      }),
    } : null;

    const response = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message, context: context }),
    });

    const data = await response.json();
    typing.remove();

    if (!response.ok || !data.success) {
      errorBox.textContent = data.message || "The assistant could not answer that.";
      errorBox.classList.remove("d-none");
      return;
    }

    addChatMessage("ai", data.reply, data.source);

    if (data.note) {
      errorBox.textContent = data.note;
      errorBox.classList.remove("d-none");
    }

  } catch (error) {
    typing.remove();
    errorBox.textContent = networkMessage();
    errorBox.classList.remove("d-none");
  } finally {
    setLoading(el("chatButton"), el("chatSpinner"), el("chatButtonText"),
               false, "Asking…", "Ask AI");
  }
}

/* ----------------------------- wiring ---------------------------------- */

document.addEventListener("DOMContentLoaded", function () {
  el("compareForm").addEventListener("submit", handleCompare);
  el("chatForm").addEventListener("submit", handleChat);

  // Example question chips fill the chat box and send.
  el("chatSuggestions").querySelectorAll(".chip").forEach(function (chip) {
    chip.addEventListener("click", function () {
      el("chatInput").value = chip.textContent.trim();
      el("chatForm").requestSubmit();
    });
  });

  checkBackend();
  loadExamples();
});