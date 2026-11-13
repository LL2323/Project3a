import csv
from datetime import datetime

from flask import Flask
from flask import render_template
from flask import request

from StockData import (
    CHART_TYPES,
    TIME_SERIES,
    StockDataError,
    fetch_data,
    filter_series,
    build_chart
)

app = Flask(__name__)

def load_stocks():

    stocks = []

    with open("stocks.csv") as file:

        reader = csv.DictReader(file)

        for row in reader:

            stocks.append(row["Symbol"])

    return stocks


@app.route("/", methods=["GET", "POST"])
def index():

    stocks = load_stocks()

    errors = []

    chart = None

    form_data = request.form

    if request.method == "POST":

        symbol = form_data.get("symbol", "")
        chart_type = form_data.get("chart_type", "")
        time_series = form_data.get("time_series", "")

        try:

            start = datetime.strptime(
                form_data.get("start_date", ""),
                "%Y-%m-%d"
            ).date()

            end = datetime.strptime(
                form_data.get("end_date", ""),
                "%Y-%m-%d"
            ).date()

        except ValueError:

            errors.append("Enter valid start and end dates.")

            start = None
            end = None

        if symbol not in stocks:

            errors.append("Choose a valid stock symbol.")

        if chart_type not in CHART_TYPES:

            errors.append("Choose a valid chart type.")

        if time_series not in TIME_SERIES:

            errors.append("Choose a valid time series.")

        if start and end:

            if start > datetime.today().date():

                errors.append("Start date cannot be in the future.")

            if end > datetime.today().date():

                errors.append("End date cannot be in the future.")

            if end <= start:

                errors.append("End date must be after start date.")

        if not errors:

            series_name, function, series_key, params = TIME_SERIES[time_series]

            try:

                raw = fetch_data(
                    symbol,
                    function,
                    params
                )

                data = filter_series(
                    raw,
                    series_key,
                    start,
                    end
                )

                if not data[0]:

                    errors.append(
                        "No data found for those dates."
                    )

                else:

                    chart = build_chart(
                        CHART_TYPES[chart_type][1],
                        symbol,
                        series_name,
                        start,
                        end,
                        data
                    ).render_data_uri()

            except StockDataError as e:

                errors.append(str(e))

    return render_template(
        "index.html",
        stocks=stocks,
        chart_types=CHART_TYPES,
        time_series=TIME_SERIES,
        form_data=form_data,
        errors=errors,
        chart=chart
    )

app.run(host="0.0.0.0")