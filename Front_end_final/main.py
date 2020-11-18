from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/map")
def map_function():
    return render_template('map2.html', title='Map')

if __name__ == '__main__':
    app.run(debug=True)