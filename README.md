from flask import Flask, request, render_template_string

app = Flask(__name__)

# =========================================================
# PG DATA
# =========================================================

pgs = [
    {
        "id": 1,
        "name": "Sri Lakshmi PG",
        "location": "Guntur",
        "rent": 6000,
        "type": "Girls",
        "room": "2 Sharing",
        "food": "Available",
        "wifi": "Available",
        "ac": "Available",
        "phone": "9876543210",
        "description": "Clean and comfortable PG near colleges and shopping areas."
    },

    {
        "id": 2,
        "name": "Sai Residency PG",
        "location": "Vijayawada",
        "rent": 7000,
        "type": "Boys",
        "room": "2 Sharing",
        "food": "Available",
        "wifi": "Available",
        "ac": "Available",
        "phone": "9876543211",
        "description": "Affordable PG with food, Wi-Fi and spacious rooms."
    },

    {
        "id": 3,
        "name": "Royal Stay PG",
        "location": "Guntur",
        "rent": 5500,
        "type": "Girls",
        "room": "3 Sharing",
        "food": "Not Available",
        "wifi": "Available",
        "ac": "Not Available",
        "phone": "9876543212",
        "description": "Budget-friendly PG suitable for students."
    },

    {
        "id": 4,
        "name": "Student Home",
        "location": "Hyderabad",
        "rent": 8000,
        "type": "Co-living",
        "room": "Single",
        "food": "Available",
        "wifi": "Available",
        "ac": "Available",
        "phone": "9876543213",
        "description": "Modern student accommodation near universities."
    },

    {
        "id": 5,
        "name": "Green View PG",
        "location": "Hyderabad",
        "rent": 6500,
        "type": "Boys",
        "room": "3 Sharing",
        "food": "Available",
        "wifi": "Available",
        "ac": "Not Available",
        "phone": "9876543214",
        "description": "Peaceful PG with excellent connectivity."
    }
]


# =========================================================
# CSS
# =========================================================

CSS = """

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background: #f5f7fb;
    color: #222;
}

/* NAVBAR */

.navbar {
    background: #4f46e5;
    color: white;
    padding: 18px 8%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 25px;
    font-weight: bold;
}

.navbar a {
    color: white;
    text-decoration: none;
    margin-left: 25px;
}

/* HERO */

.hero {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    text-align: center;
    padding: 70px 20px;
}

.hero h1 {
    font-size: 45px;
    margin-bottom: 15px;
}

.hero p {
    font-size: 18px;
}

/* SEARCH */

.search-box {
    background: white;
    width: 90%;
    max-width: 900px;
    margin: -35px auto 40px;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.search-form {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.search-form input,
.search-form select {
    padding: 13px;
    border: 1px solid #ddd;
    border-radius: 8px;
    flex: 1;
    min-width: 150px;
}

.search-btn {
    background: #4f46e5;
    color: white;
    border: none;
    padding: 13px 25px;
    border-radius: 8px;
    cursor: pointer;
}

/* PG SECTION */

.section {
    padding: 20px 8% 60px;
}

.section h2 {
    text-align: center;
    margin-bottom: 30px;
}

/* CARDS */

.pg-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 25px;
}

.pg-card {
    background: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    transition: 0.3s;
}

.pg-card:hover {
    transform: translateY(-5px);
}

.pg-image {
    height: 180px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 60px;
}

.pg-content {
    padding: 20px;
}

.pg-content h3 {
    color: #4f46e5;
    margin-bottom: 10px;
}

.pg-content p {
    margin: 8px 0;
    color: #555;
}

.price {
    color: #16a34a !important;
    font-size: 20px;
    font-weight: bold;
}

.tag {
    display: inline-block;
    background: #eef2ff;
    color: #4f46e5;
    padding: 5px 10px;
    border-radius: 20px;
    margin: 3px;
    font-size: 12px;
}

.card-buttons {
    display: flex;
    gap: 10px;
    margin-top: 15px;
}

.details-btn {
    background: #4f46e5;
    color: white;
    text-decoration: none;
    padding: 10px;
    border-radius: 7px;
    flex: 1;
    text-align: center;
}

.favorite-btn {
    background: #fee2e2;
    border: none;
    padding: 10px 15px;
    border-radius: 7px;
    cursor: pointer;
    font-size: 18px;
}

/* DETAILS */

.details {
    max-width: 700px;
    background: white;
    margin: 50px auto;
    padding: 35px;
    border-radius: 15px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

.details h1 {
    color: #4f46e5;
    margin-bottom: 20px;
}

.detail-item {
    padding: 12px 0;
    border-bottom: 1px solid #eee;
}

.contact {
    display: block;
    background: #16a34a;
    color: white;
    text-decoration: none;
    text-align: center;
    padding: 14px;
    margin-top: 25px;
    border-radius: 8px;
}

.back {
    display: block;
    text-align: center;
    margin-top: 15px;
    color: #4f46e5;
    text-decoration: none;
}

/* FOOTER */

footer {
    background: #111827;
    color: white;
    text-align: center;
    padding: 30px;
    margin-top: 40px;
}

/* MOBILE */

@media(max-width:600px) {

    .navbar {
        flex-direction: column;
        gap: 10px;
    }

    .hero h1 {
        font-size: 32px;
    }

    .search-form {
        flex-direction: column;
    }

    .search-form input,
    .search-form select,
    .search-btn {
        width: 100%;
    }
}

"""


# =========================================================
# HTML TEMPLATE
# =========================================================

HOME_HTML = """

<!DOCTYPE html>

<html>

<head>

<title>PGFinder</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

{{ css }}

</style>

</head>


<body>


<!-- NAVBAR -->

<div class="navbar">

<div class="logo">
🏠 PGFinder
</div>

<div>

<a href="/">Home</a>

<a href="#pgs">PGs</a>

</div>

</div>


<!-- HERO -->

<section class="hero">

<h1>Find Your Perfect PG</h1>

<p>Search affordable and comfortable PG accommodations near you.</p>

</section>


<!-- SEARCH -->

<div class="search-box">

<form class="search-form" method="GET" action="/">

<input
type="text"
name="location"
placeholder="📍 Enter location"
value="{{ location }}"
>


<select name="type">

<option value="">All Types</option>

<option value="Boys" {% if selected_type == "Boys" %}selected{% endif %}>
Boys
</option>

<option value="Girls" {% if selected_type == "Girls" %}selected{% endif %}>
Girls
</option>

<option value="Co-living" {% if selected_type == "Co-living" %}selected{% endif %}>
Co-living
</option>

</select>


<select name="maxrent">

<option value="">Any Rent</option>

<option value="5000">Below ₹5,000</option>

<option value="6000">Below ₹6,000</option>

<option value="7000">Below ₹7,000</option>

<option value="8000">Below ₹8,000</option>

</select>


<button class="search-btn" type="submit">
🔍 Search
</button>

</form>

</div>


<!-- PG LIST -->

<section class="section" id="pgs">

<h2>
Available PGs
</h2>


{% if pgs %}

<div class="pg-container">


{% for pg in pgs %}


<div class="pg-card">


<div class="pg-image">
🏠
</div>


<div class="pg-content">

<h3>
{{ pg.name }}
</h3>


<p>
📍 {{ pg.location }}
</p>


<p class="price">
₹{{ pg.rent }}/month
</p>


<span class="tag">
{{ pg.type }}
</span>

<span class="tag">
{{ pg.room }}
</span>


<p>
🍴 Food: {{ pg.food }}
</p>


<p>
📶 Wi-Fi: {{ pg.wifi }}
</p>


<div class="card-buttons">

<a
class="details-btn"
href="/pg/{{ pg.id }}"
>
View Details
</a>


<button
class="favorite-btn"
onclick="favoritePG('{{ pg.name }}')"
>
❤️
</button>

</div>


</div>

</div>


{% endfor %}


</div>


{% else %}

<p style="text-align:center;">
❌ No PGs found. Try another location or filter.
</p>

{% endif %}


</section>


<footer>

<p>
© 2026 PGFinder | Find. Compare. Stay.
</p>

</footer>


<script>

function favoritePG(name) {

    let favorites =
        JSON.parse(localStorage.getItem("favorites")) || [];

    if (!favorites.includes(name)) {

        favorites.push(name);

        localStorage.setItem(
            "favorites",
            JSON.stringify(favorites)
        );

        alert(name + " added to favorites ❤️");

    } else {

        alert(name + " is already in favorites.");

    }

}

</script>


</body>

</html>

"""


# =========================================================
# DETAILS PAGE
# =========================================================

DETAILS_HTML = """

<!DOCTYPE html>

<html>

<head>

<title>{{ pg.name }} - PGFinder</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

{{ css }}

</style>

</head>


<body>


<div class="navbar">

<div class="logo">
🏠 PGFinder
</div>

<a href="/">
← Back Home
</a>

</div>


<div class="details">


<h1>
{{ pg.name }}
</h1>


<div class="detail-item">

<strong>📍 Location:</strong>

{{ pg.location }}

</div>


<div class="detail-item">

<strong>💰 Monthly Rent:</strong>

₹{{ pg.rent }}

</div>


<div class="detail-item">

<strong>👤 PG Type:</strong>

{{ pg.type }}

</div>


<div class="detail-item">

<strong>🛏 Room:</strong>

{{ pg.room }}

</div>


<div class="detail-item">

<strong>🍴 Food:</strong>

{{ pg.food }}

</div>


<div class="detail-item">

<strong>📶 Wi-Fi:</strong>

{{ pg.wifi }}

</div>


<div class="detail-item">

<strong>❄️ AC:</strong>

{{ pg.ac }}

</div>


<div class="detail-item">

<strong>📝 Description:</strong>

{{ pg.description }}

</div>


<a
class="contact"
href="tel:{{ pg.phone }}"
>
📞 Contact Owner
</a>


<a
class="back"
href="/"
>
← Back to PGs
</a>


</div>


<footer>

<p>
© 2026 PGFinder
</p>

</footer>


</body>

</html>

"""


# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/")
def home():

    location = request.args.get("location", "")

    selected_type = request.args.get("type", "")

    maxrent = request.args.get("maxrent", "")


    results = pgs


    # LOCATION FILTER

    if location:

        results = [

            pg for pg in results

            if location.lower()
            in pg["location"].lower()

        ]


    # TYPE FILTER

    if selected_type:

        results = [

            pg for pg in results

            if pg["type"] == selected_type

        ]


    # RENT FILTER

    if maxrent:

        try:

            max_rent_value = int(maxrent)

            results = [

                pg for pg in results

                if pg["rent"] <= max_rent_value

            ]

        except ValueError:

            pass


    return render_template_string(

        HOME_HTML,

        pgs=results,

        location=location,

        selected_type=selected_type,

        css=CSS

    )


# =========================================================
# PG DETAILS ROUTE
# =========================================================

@app.route("/pg/<int:pg_id>")
def details(pg_id):

    pg = next(

        (pg for pg in pgs if pg["id"] == pg_id),

        None

    )


    if pg is None:

        return """

        <h1>PG Not Found</h1>

        <a href="/">Go Back</a>

        """, 404


    return render_template_string(

        DETAILS_HTML,

        pg=pg,

        css=CSS

    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)