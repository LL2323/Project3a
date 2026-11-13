## Stock Data Visualizer

This project uses Flask and the Alpha Vantage API to display stock data.

Run Locally

1. Install requirements

pip install -r requirements.txt

2. Set your Alpha Vantage API key

PowerShell:

$env:ALPHAVANTAGE_API_KEY="your_key"

3. Run

python app.py

4. Open

http://localhost:5000

Docker

docker compose up --build
