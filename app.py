import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Official IPLT20 S3 feed – same data as iplt20.com points table
POINTS_URL = "https://ipl-stats-sports-mechanic.s3.ap-south-1.amazonaws.com/ipl/feeds/stats/284-groupstandings.js"

@app.route("/ipl-points")
def ipl_points():
    try:
        resp = requests.get(POINTS_URL, timeout=10)
        resp.raise_for_status()
        text = resp.text

        # Strip JSONP wrapper: ongroupstandings({...});
        text = text.replace("ongroupstandings(", "").strip()
        if text.endswith(");"):
            text = text[:-2]

        import json
        data = json.loads(text)
        points = data.get("points", [])

        standings = []
        for p in points:
            standings.append({
                "pos": int(p.get("OrderNo", 0)),
                "team": p.get("TeamCode", ""),
                "p":   int(p.get("Matches", 0)),
                "w":   int(p.get("Wins", 0)),
                "l":   int(p.get("Loss", 0)),
                "nr":  int(p.get("NoResult", 0)),
                "nrr": p.get("NetRunRate", "0"),
                "pts": int(p.get("Points", 0))
            })

        return jsonify(standings)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
