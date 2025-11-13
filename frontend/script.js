document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  document.getElementById("output").innerHTML = "<p>Analyzing...</p>";

  const res = await fetch("/review", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  document.getElementById("output").innerHTML = `
    <h2>Results</h2>
    <p><b>Language:</b> ${data.language}</p>
    <p><b>Summary:</b> ${data.summary}</p>
    <h3>Errors:</h3>
    <pre>${JSON.stringify(data.errors, null, 2)}</pre>
    <h3>Suggestions:</h3>
    <pre>${JSON.stringify(data.suggestions, null, 2)}</pre>
    <h3>Static Checks:</h3>
    <pre>${JSON.stringify(data.static, null, 2)}</pre>
  `;
});