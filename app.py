from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the CSV once on startup
df = pd.read_csv('euro.csv')
df['DATE'] = pd.to_datetime(df['DATE']).dt.date  # Ensure proper date type

@app.route('/get-tt-sell', methods=['GET'])
def get_tt_sell():
    date_str = request.args.get('date')  # Expecting yyyy-mm-dd format
    if not date_str:
        return jsonify({"error": "Missing 'date' parameter"}), 400

    try:
        input_date = pd.to_datetime(date_str).date()
    except Exception:
        return jsonify({"error": "Invalid date format, use yyyy-mm-dd"}), 400

    row = df[df['DATE'] == input_date]
    if row.empty:
        return jsonify({"error": f"No TT Sell rate found for {date_str}"}), 404

    tt_buy_value = row.iloc[0]['TT BUY']
    return jsonify({
        "date": date_str,
        "tt_buy": tt_buy_value
    })

if __name__ == '__main__':
    app.run(debug=True)