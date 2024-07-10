async function checkPrice() {
    const stockTicker = document.getElementById('stock_ticker').value;
    const response = await fetch(`/recent_stock_data?stock_ticker=${stockTicker}`);
    const data = await response.json();

    if (data.error) {
        document.getElementById('today_price').innerText = data.error;
    } else {
        document.getElementById('today_price').innerText = `Today's Price: ${data[data.length - 1].Adj_Close || data[data.length - 1].Close}`;
        showSection('stock_info');
    }
}

async function fetchRecentNews() {
    const stockTicker = document.getElementById('stock_ticker').value;
    const response = await fetch(`/recent_news?stock_ticker=${stockTicker}`);
    const data = await response.json();

    if (data.error) {
        document.getElementById('news_data').innerText = data.error;
    } else {
        displayNewsData(data);
        showSection('news');
    }
}

function displayStockDataTable(data) {
    let table = '<table><tr><th>Date</th><th>Open</th><th>High</th><th>Low</th><th>Close</th><th>Volume</th></tr>';
    data.slice(-5).forEach(row => {
        table += `<tr>
            <td>${new Date(row.Date).toDateString()}</td>
            <td>${row.Open}</td>
            <td>${row.High}</td>
            <td>${row.Low}</td>
            <td>${row.Close}</td>
            <td>${row.Volume}</td>
        </tr>`;
    });
    table += '</table>';
    document.getElementById('stock_table').innerHTML = table;
}

function displayNewsData(data) {
    let newsHtml = '';
    data.forEach(news => {
        newsHtml += `<div class="news-item">
            <h3>${news.description || 'No headline available'}</h3>
            <p>Sentiment: ${news.sentiment || 'N/A'}</p>
            <a href="${news.url}" target="_blank">Read more</a>
        </div>`;
    });
    document.getElementById('news_data').innerHTML = newsHtml;
}

async function visualizeData(type) {
    const stockTicker = document.getElementById('stock_ticker').value;
    const response = await fetch(`/recent_stock_data?stock_ticker=${stockTicker}`);
    const data = await response.json();

    if (type === 'table') {
        displayStockDataTable(data);
        showSection('stock_info');
    } else if (type === 'chart') {
        displayStockDataChart(data);
        showSection('stock_info');
    }
}

function displayStockDataChart(data) {
    const ctx = document.getElementById('stock_chart').getContext('2d');
    const labels = data.slice(-5).map(row => new Date(row.Date).toDateString());
    const prices = data.slice(-5).map(row => row["Close"]);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Price',
                data: prices,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'category'
                },
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

async function predictPrice() {
    const stockTicker = document.getElementById('stock_ticker').value;
    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ stock_ticker: stockTicker })
    });
    const data = await response.json();

    if (data.error) {
        document.getElementById('prediction_result').innerText = data.error;
    } else {
        document.getElementById('prediction_result').innerText = `Tomorrow's Predicted Price: ${data.tomorrow_prediction}`;
        document.getElementById('decision').innerText = `Decision: ${data.decision}`;
        document.getElementById('certainty').innerText = `Certainty: ${(data.certainty || 0).toFixed(2)}%`;
        document.getElementById('decision').style.color = data.decision === 'BUY' ? 'green' : 'red';
        showSection('prediction');
    }
}

function showSection(sectionId) {
    document.getElementById('stock_info').style.display = 'none';
    document.getElementById('prediction').style.display = 'none';
    document.getElementById('news').style.display = 'none';
    document.getElementById(sectionId).style.display = 'block';
}
