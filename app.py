from flask import Flask, request, render_template, render_template_string
import requests
import html
import re
from urllib.parse import quote

app = Flask(__name__)

# ============================================================
# FREE / NO API KEY CONFIGURATION
# Uses OpenStreetMap + Nominatim + Overpass API
# ============================================================

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# OSM asks applications to identify themselves.
HEADERS = {
    "User-Agent": "PGFinder/1.0 (student project)"
}

# Maximum number of accommodation results displayed.
MAX_RESULTS = 200


# ============================================================
# CSS
# ============================================================

CSS = """
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, sans-serif;
    background: #f4f6fb;
    color: #222;
}

.navbar {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    padding: 18px 7%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 27px;
    font-weight: bold;
}

.navbar a {
    color: white;
    text-decoration: none;
    margin-left: 20px;
}

.hero {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    text-align: center;
    padding: 70px 20px 90px;
}

.hero h1 {
    font-size: 45px;
    margin-bottom: 15px;
}

.hero p {
    font-size: 18px;
}

.search-container {
    width: 90%;
    max-width: 1100px;
    margin: -45px auto 40px;
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.search-form {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 12px;
}

.search-input {
    padding: 16px;
    border: 1px solid #ddd;
    border-radius: 10px;
    font-size: 16px;
}

.search-button {
    background: #4f46e5;
    color: white;
    border: none;
    padding: 16px 30px;
    border-radius: 10px;
    font-size: 16px;
    cursor: pointer;
}

.search-button:hover {
    background: #3730a3;
}

.results-section {
    width: 90%;
    max-width: 1200px;
    margin: auto;
    padding-bottom: 60px;
}

.results-title {
    text-align: center;
    margin-bottom: 30px;
}

.results-title h2 {
    font-size: 30px;
}

.results-title p {
    color: #666;
    margin-top: 8px;
}

.pg-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
    gap: 25px;
}

.pg-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 5px 18px rgba(0,0,0,0.09);
    transition: 0.25s;
}

.pg-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.14);
}

.pg-top {
    height: 150px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 65px;
}

.pg-content {
    padding: 20px;
}

.pg-name {
    font-size: 21px;
    color: #4f46e5;
    margin-bottom: 10px;
}

.address {
    color: #555;
    line-height: 1.5;
    margin-bottom: 12px;
}

.rating {
    color: #f59e0b;
    font-weight: bold;
    margin-bottom: 12px;
}

.tag {
    display: inline-block;
    background: #eef2ff;
    color: #4f46e5;
    padding: 6px 10px;
    border-radius: 20px;
    font-size: 12px;
    margin: 3px 3px 10px 0;
}

.card-buttons {
    display: flex;
    gap: 8px;
    margin-top: 15px;
}

.details-button {
    flex: 1;
    background: #4f46e5;
    color: white;
    text-decoration: none;
    padding: 11px;
    border-radius: 8px;
    text-align: center;
}

.map-button {
    background: #16a34a;
    color: white;
    text-decoration: none;
    padding: 11px 14px;
    border-radius: 8px;
}

.details-container {
    width: 90%;
    max-width: 750px;
    background: white;
    margin: 50px auto;
    padding: 35px;
    border-radius: 18px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

.details-container h1 {
    color: #4f46e5;
    margin-bottom: 25px;
}

.detail-row {
    padding: 15px 0;
    border-bottom: 1px solid #eee;
}

.detail-label {
    font-weight: bold;
    display: block;
    margin-bottom: 5px;
}

.action-button {
    display: block;
    text-align: center;
    margin-top: 25px;
    padding: 14px;
    background: #4f46e5;
    color: white;
    text-decoration: none;
    border-radius: 9px;
}

.back-button {
    display: block;
    text-align: center;
    margin-top: 15px;
    color: #4f46e5;
    text-decoration: none;
}

.message {
    background: white;
    padding: 35px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
}

.error {
    color: #dc2626;
}

.info {
    color: #555;
    margin-top: 12px;
    line-height: 1.6;
}

footer {
    background: #111827;
    color: white;
    text-align: center;
    padding: 30px;
    margin-top: 50px;
}

@media(max-width: 650px) {
    .navbar {
        flex-direction: column;
        gap: 10px;
    }

    .hero h1 {
        font-size: 32px;
    }

    .search-form {
        grid-template-columns: 1fr;
    }
}
"""


# ============================================================
# LOCATION / GEOCODING
# ============================================================

def geocode_location(location):
    """Find the searched location and return a useful bounding box."""

    try:
        response = requests.get(
            NOMINATIM_URL,
            params={
                "q": location,
                "format": "jsonv2",
                "limit": 1
            },
            headers=HEADERS,
            timeout=20
        )
        response.raise_for_status()

        data = response.json()

        if not data:
            return None, "Location could not be found."

        result = data[0]

        lat = float(result["lat"])
        lon = float(result["lon"])

        # Nominatim returns south, north, west, east.
        bbox = [float(x) for x in result["boundingbox"]]

        return {
            "lat": lat,
            "lon": lon,
            "bbox": bbox,
            "display_name": result.get("display_name", location)
        }, None

    except requests.RequestException as error:
        return None, f"Location service error: {error}"

    except (ValueError, KeyError, IndexError):
        return None, "Invalid location data returned by the map service."


# ============================================================
# OVERPASS SEARCH
# ============================================================

def make_search_bbox(geo):
    """
    Create a practical search box.

    For a city/area, use its Nominatim bounding box.
    For very large searches such as a country, use roughly
    a 50 km radius around the geocoded center so Overpass
    does not receive an enormous worldwide query.
    """

    south, north, west, east = geo["bbox"]
    lat = geo["lat"]
    lon = geo["lon"]

    # If bbox is extremely large, use about 50 km around center.
    if (north - south) > 1.0 or (east - west) > 1.0:
        lat_delta = 0.45
        lon_delta = 0.45
        south = max(-90, lat - lat_delta)
        north = min(90, lat + lat_delta)
        west = max(-180, lon - lon_delta)
        east = min(180, lon + lon_delta)

    return south, west, north, east


def search_overpass(location, geo):
    """
    Search OpenStreetMap for hostels, student accommodation,
    guest houses, hotels, dormitories, co-living and places
    whose names suggest PG/student accommodation.
    """

    south, west, north, east = make_search_bbox(geo)

    # Keep the query focused on accommodation.
    query = f"""
    [out:json][timeout:45];

    (
      nwr["amenity"="student_accommodation"]({south},{west},{north},{east});
      nwr["tourism"="hostel"]({south},{west},{north},{east});
      nwr["tourism"="guest_house"]({south},{west},{north},{east});
      nwr["tourism"="hotel"]({south},{west},{north},{east});
      nwr["tourism"="motel"]({south},{west},{north},{east});
      nwr["tourism"="apartment"]({south},{west},{north},{east});
      nwr["building"="dormitory"]({south},{west},{north},{east});
      nwr["residential"="student_accommodation"]({south},{west},{north},{east});

      nwr["name"~"PG|Paying Guest|paying guest|Hostel|hostel|Student|student|Dorm|dorm|Coliving|coliving|Co-Living|co-living",i]
      ({south},{west},{north},{east});
    );

    out center tags;
    """

    try:
        response = requests.post(
            OVERPASS_URL,
            data=query,
            headers=HEADERS,
            timeout=60
        )
        response.raise_for_status()

        data = response.json()
        return data.get("elements", []), None

    except requests.RequestException as error:
        return [], f"OpenStreetMap search error: {error}"

    except ValueError:
        return [], "OpenStreetMap returned invalid data."


# ============================================================
# CONVERT OSM RESULTS TO PG RESULTS
# ============================================================

def element_coordinates(element):
    """Get latitude/longitude from a node or a way/relation center."""

    if element.get("type") == "node":
        return element.get("lat"), element.get("lon")

    center = element.get("center", {})
    return center.get("lat"), center.get("lon")


def element_address(tags):
    """Build a readable address from OSM address tags."""

    parts = []

    for key in [
        "addr:housenumber",
        "addr:street",
        "addr:suburb",
        "addr:neighbourhood",
        "addr:city",
        "addr:town",
        "addr:state",
        "addr:postcode",
        "addr:country"
    ]:
        value = tags.get(key)
        if value and value not in parts:
            parts.append(value)

    if parts:
        return ", ".join(parts)

    return tags.get("description") or tags.get("addr:full") or "Address unavailable"


def accommodation_type(tags):
    """Return a friendly category."""

    if tags.get("amenity") == "student_accommodation":
        return "Student accommodation"

    if tags.get("tourism") == "hostel":
        return "Hostel"

    if tags.get("tourism") == "guest_house":
        return "Guest house"

    if tags.get("tourism") == "hotel":
        return "Hotel"

    if tags.get("building") == "dormitory":
        return "Dormitory"

    if tags.get("residential") == "student_accommodation":
        return "Student accommodation"

    if tags.get("tourism"):
        return tags["tourism"].replace("_", " ").title()

    return "Accommodation"


def convert_results(elements):
    """Convert OSM elements into the format used by the HTML."""

    combined = {}

    for element in elements:
        tags = element.get("tags", {})
        name = tags.get("name")

        # Ignore unnamed map objects because they are not useful to users.
        if not name:
            continue

        lat, lon = element_coordinates(element)

        if lat is None or lon is None:
            continue

        osm_id = f'{element.get("type")}_{element.get("id")}'

        maps_url = (
            f"https://www.openstreetmap.org/"
            f"{element.get('type')}/{element.get('id')}"
        )

        website = (
            tags.get("website")
            or tags.get("contact:website")
        )

        phone = (
            tags.get("phone")
            or tags.get("contact:phone")
        )

        category = accommodation_type(tags)

        item = {
            "id": osm_id,
            "osm_type": element.get("type"),
            "osm_id_number": element.get("id"),
            "name": name,
            "address": element_address(tags),
            "rating": None,
            "rating_count": None,
            "maps_url": maps_url,
            "website": website,
            "phone": phone,
            "primary_type": category,
            "lat": lat,
            "lon": lon,
            "description": tags.get("description"),
            "opening_hours": tags.get("opening_hours"),
            "gender": tags.get("gender"),
        }

        combined[osm_id] = item

    results = list(combined.values())

    # Put likely PG/student places first.
    def sort_score(item):
        text = (
            item["name"] + " " +
            item["primary_type"] + " " +
            (item["description"] or "")
        ).lower()

        score = 0

        for keyword in [
            "pg",
            "paying guest",
            "student",
            "hostel",
            "dorm",
            "coliving",
            "co-living"
        ]:
            if keyword in text:
                score += 1

        return score

    results.sort(
        key=lambda x: (
            sort_score(x),
            x["name"].lower()
        ),
        reverse=True
    )

    return results[:MAX_RESULTS]


# ============================================================
# HTML
# ============================================================

HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>PGFinder - Worldwide PG Search</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{{ css }}</style>
</head>

<body>

<nav class="navbar">
<div class="logo">🏠 PGFinder</div>
<div><a href="/">Home</a></div>
</nav>

<section class="hero">
<h1>Find PGs Anywhere 🌍</h1>
<p>Search PGs, hostels, student accommodation and co-living spaces worldwide.</p>
</section>

<div class="search-container">
<form class="search-form" method="GET" action="/">
<input
    class="search-input"
    type="text"
    name="location"
    value="{{ location }}"
    placeholder="🌍 Enter city, area or country — e.g. Guntur, Hyderabad, Dubai, London"
    required
>
<button class="search-button" type="submit">🔍 Search</button>
</form>
</div>

<section class="results-section">

{% if searched %}

<div class="results-title">
<h2>PGs & Accommodation in {{ location }}</h2>
<p>Found {{ pgs|length }} unique results</p>
</div>

{% if error %}
<div class="message error">
{{ error }}
</div>
{% endif %}

{% if pgs %}

<div class="pg-grid">

{% for pg in pgs %}
<div class="pg-card">

<div class="pg-top">🏠</div>

<div class="pg-content">

<h3 class="pg-name">{{ pg.name }}</h3>

<p class="address">📍 {{ pg.address }}</p>

{% if pg.primary_type %}
<span class="tag">{{ pg.primary_type }}</span>
{% endif %}

{% if pg.phone %}
<p style="margin-top:8px;">📞 {{ pg.phone }}</p>
{% endif %}

<div class="card-buttons">

<a class="details-button" href="/place/{{ pg.id }}">
View Details
</a>

<a class="map-button" href="{{ pg.maps_url }}" target="_blank">
📍 Map
</a>

</div>

</div>
</div>
{% endfor %}

</div>

{% else %}

<div class="message">
<h2>No PGs found</h2>
<p>Try a nearby city, area, or another spelling.</p>
<p class="info">
Results come from OpenStreetMap. If a PG is not mapped there,
PGFinder cannot display it yet.
</p>
</div>

{% endif %}

{% else %}

<div class="message">
<h2>🌍 Search for PGs anywhere</h2>
<p>Try:</p>
<br>
<p>Guntur • Hyderabad • Bangalore • Mumbai • Dubai • London • New York</p>
</div>

{% endif %}

</section>

<footer>
<p>© 2026 PGFinder</p>
<p style="margin-top:8px;">Powered by OpenStreetMap</p>
</footer>

</body>
</html>
"""


DETAILS_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>{{ pg.name }} - PGFinder</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{{ css }}</style>
</head>

<body>

<nav class="navbar">
<div class="logo">🏠 PGFinder</div>
<a href="/">← Home</a>
</nav>

<div class="details-container">

<h1>{{ pg.name }}</h1>

<div class="detail-row">
<span class="detail-label">📍 Address</span>
{{ pg.address }}
</div>

{% if pg.primary_type %}
<div class="detail-row">
<span class="detail-label">🏠 Category</span>
{{ pg.primary_type }}
</div>
{% endif %}

{% if pg.phone %}
<div class="detail-row">
<span class="detail-label">📞 Phone</span>
{{ pg.phone }}
</div>
{% endif %}

{% if pg.opening_hours %}
<div class="detail-row">
<span class="detail-label">🕒 Opening hours</span>
{{ pg.opening_hours }}
</div>
{% endif %}

{% if pg.gender %}
<div class="detail-row">
<span class="detail-label">👥 Gender</span>
{{ pg.gender }}
</div>
{% endif %}

{% if pg.description %}
<div class="detail-row">
<span class="detail-label">ℹ️ Description</span>
{{ pg.description }}
</div>
{% endif %}

{% if pg.website %}
<a class="action-button" href="{{ pg.website }}" target="_blank">
🌐 Visit Website
</a>
{% endif %}

<a class="action-button" href="{{ pg.maps_url }}" target="_blank">
📍 Open in OpenStreetMap
</a>

<a class="back-button" href="/">
← Back to Search
</a>

</div>

<footer>
<p>© 2026 PGFinder</p>
<p style="margin-top:8px;">Powered by OpenStreetMap</p>
</footer>

</body>
</html>
"""


# ============================================================
# HOME ROUTE
# ============================================================

@app.route("/")
def home():
    location = request.args.get("location")

    if not location:
        return render_template(
            "home.html",
            location="",
            searched=False,
            pgs=[],
            error=None
        )
        
        

    geo, geo_error = geocode_location(location)

    if geo_error:
       return render_template(
        "home.html",
        location=location,
        searched=True,
        pgs=[],
        error=geo_error
    )

    raw_places, search_error = search_overpass(location, geo)

    pgs = convert_results(raw_places)

    error_message = search_error

    return render_template(
        "home.html",
        location=location,
        searched=True,
        pgs=pgs,
        error=error_message
    )


# ============================================================
# PLACE DETAILS
# ============================================================

@app.route("/place/<place_id>")
def place_details(place_id):

    match = re.match(r"^(node|way|relation)_(\d+)$", place_id)

    if not match:
        return "Invalid place ID.", 400

    osm_type = match.group(1)
    osm_id = match.group(2)

    # Query the individual OSM object.
    query = f"""
    [out:json][timeout:20];
    {osm_type}({osm_id});
    out center tags;
    """

    try:
        response = requests.post(
            OVERPASS_URL,
            data=query,
            headers=HEADERS,
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        elements = data.get("elements", [])

    except requests.RequestException as error:
        return f"OpenStreetMap error: {error}", 500

    except ValueError:
        return "OpenStreetMap returned invalid data.", 500

    if not elements:
        return "Place not found.", 404

    converted = convert_results(elements)

    if converted:
        pg = converted[0]
    else:
        element = elements[0]
        tags = element.get("tags", {})
        lat, lon = element_coordinates(element)

        pg = {
            "id": place_id,
            "name": tags.get("name", "Accommodation"),
            "address": element_address(tags),
            "primary_type": accommodation_type(tags),
            "phone": tags.get("phone"),
            "website": tags.get("website"),
            "maps_url": (
                f"https://www.openstreetmap.org/"
                f"{osm_type}/{osm_id}"
            ),
            "opening_hours": tags.get("opening_hours"),
            "gender": tags.get("gender"),
            "description": tags.get("description"),
            "lat": lat,
            "lon": lon
        }

    return render_template_string(
        DETAILS_HTML,
        css=CSS,
        pg=pg
    )


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":

    print("")
    print("======================================")
    print("       PGFINDER IS STARTING")
    print("======================================")
    print("No Google API key is required.")
    print("Using OpenStreetMap + Overpass.")
    print("")
    print("Open:")
    print("http://127.0.0.1:5000")
    print("")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
