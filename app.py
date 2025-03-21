from flask import Flask, request, render_template, redirect
import myscraper
import write_output
import search_des

# Initialize Flask app
app = Flask(__name__)

# Route: Home page
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

# Route: When user submits a product search
@app.route('/searching', methods=["GET", "POST"])
def searching():
    if request.method == "POST":
        search = request.form.get("search")
        print(f"Search query: {search}")
        myscraper.result(search)  # Run the web scraper
        return redirect('/display')
    return redirect('/')

# Route: Display results after scraping
@app.route("/display")
def display():
    write_output.write_output()  # Generate output.html from results.csv
    return render_template("output.html")

# Route: Search by product description
@app.route("/searching_des", methods=["GET", "POST"])
def results():
    if request.method == "POST":
        search = request.form.get("search_des")
        print(f"Search description: {search}")
        search_des.similarity_computation(search)
        return redirect('/display')
    return redirect('/')

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
