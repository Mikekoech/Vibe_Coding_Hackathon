document.getElementById('recipe-form').addEventListener('submit', async function(e) {
  e.preventDefault();

  const ingredients = document.getElementById('ingredients').value;
  const resultsDiv = document.getElementById('results');

  try {
    const res = await fetch('/suggest', {
      method: 'POST',
      body: new URLSearchParams({ ingredients })
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    const data = await res.json();
    if (data.recipes) {
      resultsDiv.innerHTML = `<pre>${data.recipes}</pre>`;
    } else {
      resultsDiv.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
    }
  } catch (err) {
    resultsDiv.innerHTML = `<p style="color:red;">Network error: ${err.message}</p>`;
  }
});