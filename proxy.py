import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

IPL_URL = "https://www.iplt20.com/points-table"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

@app.route("/ipl-points")
def ipl_points():
    try:
        resp = requests.get(IPL_URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # The points table has a specific class on the tbody
        table = soup.find("table", class_="points-table")
        if not table:
            table = soup.find("table")

        if not table:
            return jsonify({"error": "Table not found"}), 500

        rows = table.find_all("tr")[1:]   # skip header
        standings = []

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 8:
                continue
            try:
                entry = {
                    "pos": int(cols[0].text.strip()),
                    "team": cols[1].text.strip(),
                    "p": int(cols[2].text.strip()),
                    "w": int(cols[3].text.strip()),
                    "l": int(cols[4].text.strip()),
                    "nr": int(cols[5].text.strip()) if cols[5].text.strip().isdigit() else 0,
                    "nrr": cols[6].text.strip(),
                    "pts": int(cols[7].text.strip())
                }
                standings.append(entry)
            except (ValueError, IndexError):
                continue

        return jsonify(standings)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)