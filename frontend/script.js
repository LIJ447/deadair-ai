
async function narrate() {
  const text = document.getElementById('story').value;
  const voice = document.getElementById('voice').value;
  const formData = new FormData();
  formData.append("text", text);
  formData.append("voice", voice);

  const response = await fetch("/narrate", {
    method: "POST",
    body: formData
  });

  const data = await response.json();
  document.getElementById('player').src = data.url;
}
    