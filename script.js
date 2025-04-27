const loadBtn = document.getElementById("loadBtn");
const tokensTable = document.getElementById("tokensTable");
const ctx = document.getElementById('activityChart').getContext('2d');
let chart;

loadBtn.addEventListener("click", async () => {
  const response = await fetch("http://localhost:8000/suspicious-tokens");
  const data = await response.json();

  tokensTable.innerHTML = ""; // Clear previous data

  data.suspicious_tokens.forEach(token => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${token.token}</td>
      <td>${token.price_change_24h.toFixed(2)}%</td>
      <td>${token.social_spike}</td>
    `;
    row.addEventListener("click", () => {
      drawChart(token);
    });
    tokensTable.appendChild(row);
  });
});

function drawChart(token) {
  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Price Change %', 'Social Spike'],
      datasets: [{
        label: `${token.token} Activity`,
        data: [token.price_change_24h, token.social_spike],
        backgroundColor: ['blue', 'green']
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}
