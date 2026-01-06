from flask import Flask, request, render_template_string, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "/data/db.json"

def load_cache():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_cache(data):
    os.makedirs("/data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

HTML_PAGE = """ 
<!DOCTYPE html>
<html>
<head>
    <title>Name Cache App</title>
</head>
<body>

<h2>Enter Details</h2>
<form method="POST">
    <input name="first_name" placeholder="First Name" required><br><br>
    <input name="last_name" placeholder="Last Name" required><br><br>
    <input name="email" placeholder="Email" required><br><br>
    <input name="number" placeholder="Phone" required><br><br>
    <button type="submit">Submit</button>
</form>

<h3>Stored Data</h3>

{% if cache %}
<table border="1">
<tr>
<th>First</th><th>Last</th><th>Email</th><th>Phone</th>
</tr>
{% for item in cache %}
<tr>
<td>{{ item.first_name }}</td>
<td>{{ item.last_name }}</td>
<td>{{ item.email }}</td>
<td>{{ item.number }}</td>
</tr>
{% endfor %}
</table>
{% else %}
<p>No data</p>
{% endif %}
<form method="POST" action="/clear">
    <button type="submit" style="margin-top:10px;">
        Clear All Entries
    </button>
</form>


</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    cache = load_cache()

    if request.method == "POST":
        cache.append({
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "number": request.form["number"]
        })
        save_cache(cache)

        # 🔴 IMPORTANT LINE
        return redirect(url_for("index"))

    return render_template_string(HTML_PAGE, cache=cache)
@app.route("/clear", methods=["POST"])
def clear():
    save_cache([])  # overwrite file with empty list
    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
