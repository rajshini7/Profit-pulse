# 📈 Stock Information and Prediction Dashboard

Welcome to the Stock Information and Prediction Dashboard! This project provides a comprehensive platform to fetch, display, and predict stock information. It combines stock data visualization, recent news sentiment analysis, and prediction models to give you a detailed overview of stock performance and future trends.


## 📝 Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Component Details](#component-details)
    1. [Frontend](#frontend)
    2. [Backend](#backend)
    3. [Utilities](#utilities)
6. [API Endpoints](#api-endpoints)
7. [Contributing](#contributing)
8. [License](#license)

## 📚 Project Overview
This project is built using Flask for the backend, handling data fetching, preprocessing, and predictions, while the frontend is built using HTML, CSS, and JavaScript for an interactive user interface. The dashboard allows users to:
- Fetch and display current stock prices.
- View recent news related to a specific stock and analyze its sentiment.
- Visualize historical stock data in tabular and graphical formats.
- Predict the next day's stock price and provide a buy/sell decision with certainty.

## ✨ Features
- **Current Stock Price**: Fetch and display the latest stock price.
- **Recent News**: Get the latest news articles related to a specific stock and analyze their sentiment.
- **Data Visualization**: Visualize historical stock data in both table and chart formats.
- **Prediction**: Predict the next day's stock price and provide a buy/sell decision with a certainty percentage.

## 🚀 Installation
To get started with this project, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/stock-dashboard.git
   cd stock-dashboard
## 💻 Usage
Once the application is running, you can interact with the dashboard by:

- Entering a stock ticker in the input field.
- Clicking on the various buttons to fetch data, visualize it, or get predictions.
- Viewing the information in different sections based on your selection.

## 🛠️ Component Details

### Frontend
The frontend consists of the main HTML file (`index.html`), CSS styles (`style.css`), and JavaScript (`script.js`). It provides a clean and interactive user interface for user input and data display.

- **index.html**: Structure of the web page with sections for stock information, predictions, and news.
- **style.css**: Styling for the web page, including layout, colors, and typography.
- **script.js**: JavaScript functions to handle user interactions, fetch data from the backend, and update the DOM.

### Backend
The backend is built using Flask and handles API requests, data processing, and model predictions.

- **frontend.py**: Main Flask application file, defining routes and API endpoints.
- **models**: Contains the machine learning models used for stock price prediction.
  - `lstm_gru_news_model.py`
  - `frontendmodel.py`

### Utilities
Utility functions are defined in the `utils` directory to help with data fetching, processing, and analysis.

- **data_preprocessing.py**: Preprocesses stock data for model training.
- **plot_utils.py**: Utility functions for plotting data.
- **sentiment_analysis.py**: Analyzes the sentiment of news articles.

## 🌐 API Endpoints
The following API endpoints are available for data fetching and predictions:

- **GET /recent_stock_data**: Fetches recent stock data.
- **GET /recent_news**: Fetches recent news articles.
- **POST /predict**: Predicts the next day's stock price.

## 🤝 Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please fork the repository and create a pull request. You can also open an issue to discuss potential changes.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

Thank you for using the Stock Information and Prediction Dashboard! We hope you find it useful and informative. Happy trading!

---

**Contact Information:**

- **Email**: pranshuarora1618@gmail.com
- **GitHub**: [pranshuarora7](https://github.com/pranshuarora7)

