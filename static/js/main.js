fetch("http://localhost:8000/api/ads/")
  .then(response => response.json())
  .then(data => {
    const adsList = document.getElementById("ads-list");
    data.results.forEach(ad => {
      const li = document.createElement("li");
      li.className = "list-group-item";
      li.innerHTML = `<strong>${ad.title}</strong><br><small>Автор: ${ad.author_email}</small>`;
      adsList.appendChild(li);
    });
  })
  .catch(error => {
    console.error("Ошибка при загрузке объявлений:", error);
  });
