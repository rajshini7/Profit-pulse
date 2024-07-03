document.getElementById('stock-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const stockTicker = document.getElementById('stock-ticker').value;

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ stock_ticker: stockTicker }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (data.error) {
            alert(data.error);
            return;
        }

        // Update individual metrics
        document.getElementById('today-price').textContent = data.today_price.toFixed(2);
        document.getElementById('tomorrow-prediction').textContent = data.tomorrow_prediction.toFixed(2);
        document.getElementById('decision').textContent = data.decision;
        document.getElementById('decision').className = data.decision === "BUY" ? 'buy' : 'not-buy';

        // Clear previous data in the table
        const stockTableBody = document.getElementById('stock-data-body');
        stockTableBody.innerHTML = '';

        // Populate stock data into the table
        data.stock_data_sample.forEach(stock => {
            const row = stockTableBody.insertRow();
            row.insertCell(0).textContent = stock.Date;
            row.insertCell(1).textContent = stock.Open.toFixed(2);
            row.insertCell(2).textContent = stock.High.toFixed(2);
            row.insertCell(3).textContent = stock.Low.toFixed(2);
            row.insertCell(4).textContent = stock.Close.toFixed(2);
            row.insertCell(5).textContent = stock.Volume;
            row.insertCell(6).textContent = stock.sentiment.toFixed(2);
        });

        // Update the chart
        const labels = data.stock_data.map(d => d.Date);
        const adjCloseData = data.stock_data.map(d => d['Adj Close']);

        const ctx = document.getElementById('stock-chart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Adj Close',
                    data: adjCloseData,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    fill: false
                }]
            },
            options: {
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Price'
                        }
                    }
                }
            }
        });

        document.getElementById('result').style.display = 'block';
        document.getElementById('result').scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while fetching the prediction data.');
    }
});
