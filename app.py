from flask import Flask, render_template, request

app = Flask(__name__)

subscribers =[]

@app.route('/')
def index():
    title = "Angelos's Blog"
    return render_template("index.html", title=title)
    
@app.route('/about')
def about():
    title = "About Angelos!"
    names = ["Angelos", "Mary", "Wes", "Sally"]
    return render_template("about.html", names=names, title=title)

@app.route('/subscribe')
def subscribe():
    title = "Subscribe My Email Newsletter"
    return render_template("subscribe.html", title=title)

@app.route('/form', methods=["POST"])
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email =  request.form.get("email")
    subscribers.append(f"{first_name} {last_name} | {email}")
    title = "Thank you!"
    return render_template("form.html", title=title, subscribers=subscribers)

    #test