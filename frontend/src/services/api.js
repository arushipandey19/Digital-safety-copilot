const API = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function analyzeInput({ type, text, url, file }) {
  const form = new FormData();
  form.append("input_type", type);
  form.append("text", text || "");
  form.append("url", url || "");

  if (file) {
    form.append("image", file);
  }

  const response = await fetch(`${API}/api/analyze`, {
    method: "POST",
    body: form
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Analysis failed");
  }

  return response.json();
}
