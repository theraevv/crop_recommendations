async function predict() {
  const fields = ["N","P","K","temp","humidity","ph","rainfall"];
  const data = {};

  for (const f of fields) {
    const val = document.getElementById(f).value;

    if (val === "") {
      showError("Please fill all fields");
      return;
    }

    data[f] = parseFloat(val);
  }

  try {
    const res = await fetch("https://YOUR-RENDER-URL/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    const json = await res.json();

    if (!res.ok) {
      showError(json.error);
      return;
    }

    displayResults(json.results);

  } catch (err) {
    showError("Server not reachable");
  }
}

function showError(msg) {
  const errorDiv = document.getElementById("error");
  errorDiv.textContent = msg;
  errorDiv.classList.remove("hidden");
}

function displayResults(top3) {
  const container = document.getElementById("top3");
  container.innerHTML = "";

  top3.forEach((item, index) => {
    container.innerHTML += `
      <div>#${index+1} ${item.crop} (${item.confidence}%)</div>
    `;
  });

  document.getElementById("result").classList.remove("hidden");
}