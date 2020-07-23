import json
import os
import random
from gtts import gTTS
from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory
from flask_session import Session
import api

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024 * 1024


@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static', 'js'),   filename)  

@app.route("/")
def index():
    if session.get("page") == None:
        session["page"] = 1

    with open('books.json','r') as json_file:
        books = json.load(json_file)
    
    if session["page"] == 1:
        data = books["books"]
    else:
        data = books[f"book"+str(session["page"])]
    
    lp = False
    if len(data)!=6:
        lp = True

    return render_template("home.html", data = data, page = session["page"], search = False, l = lp)

@app.route("/page/<int:p>")
def page(p):
    session["page"] = p
    return redirect(url_for("index"))

@app.route("/search", methods=['POST'])
def search():
    item = request.form.get('search')
    with open('books.json','r') as f:
        books = json.load(f)
    
    data = {"books": []}
    count = 0

    for b in books:
        for book in books[b]:
            if item in book['name'] or item in book['author']:
                data["books"].append(book)
                count+=1

    if(count>0):
        return render_template("home.html", data = data["books"], search = True)
    else:
        return render_template("home.html", data = None, search = True)

@app.route("/user", methods = ['GET', 'POST'])
def user():
    if request.method == 'POST':
        onlyfiles = next(os.walk("./static/temp"))[2]
        temp = str(random.randint(10000,99999))+str(len(onlyfiles))

        text = request.form.get('text')
        test = gTTS(text,lang='GU')
        
        path = "./static/temp/"+str(temp)+".mp3"

        test.save(path)

        session["mpname"] = str(temp)+".mp3"

        return render_template("user.html", data = session["mpname"])
    else:
        if session.get("datai") == None:
            return render_template("user.html", data = None, datai = None)
        else:
            return render_template("user.html", data = None, datai = session["datai"])

@app.route("/ito", methods = ['GET','POST'])
def ito():
    if request.method == 'POST':
        f = request.files['image']
        f.save(os.path.join("./static/temp",f.filename))

        session["datai"] = api.image_to_text(os.path.join("./static/temp",f.filename))

        return redirect(url_for("user"))
    else:
        return render_template("image.html")

app.config["IMAGE_UPLOAD"] = "./static/images"
app.config["AUDIO_UPLOAD"] = "./static/audios"
app.config["PDF_UPLOAD"] = "./static/pdfs"

@app.route("/secret", methods = ['GET', 'POST'])
def secret():
    if request.method == 'POST':
        name = request.form.get('name')
        author = request.form.get('author')
        details = request.form.get('details')

        f1 = request.files['image']
        f1.save(os.path.join(app.config["IMAGE_UPLOAD"], f1.filename))

        f2 = request.files.getlist('audio[]')
        audios = []
        for audio in f2:
            audio.save(os.path.join(app.config["AUDIO_UPLOAD"], audio.filename))
            audios.append(str(audio.filename))

        f3 = request.files['pdf']
        f3.save(os.path.join(app.config["PDF_UPLOAD"], f3.filename))

        with open('books.json','r+', encoding='utf-8') as json_file:
            books = json.load(json_file)

            count = 1
            for book in books:
                if len(books[book]) < 6:
                    books[book].append({"name" : name,"author" : author,"details" : details,"image" : f1.filename,"audio" : audios,"pdf" : f3.filename})
                count+=1
            else:
                d = {f"book{count}":[{"name" : name,"author" : author,"details" : details,"image" : f1.filename,"audio" : audios,"pdf" : f3.filename}]}
                books.update(d)
            json_file.seek(0)
            json.dump(books, json_file)

        return render_template("upload.html", message="Y")
    else:
        return render_template("upload.html", message="N")

@app.route("/<string:name>", methods=['GET','POST'])
def book1(name):
    session["bname"] = name
    return redirect(url_for("book"))

@app.route("/book", methods=['GET','POST'])
def book():
    with open('books.json','r') as f:
        books = json.load(f)
    
    for b in books:
        for book in books[b]:
            if book['name'] == session.get("bname"):
                return render_template("book.html", data = book)
    else:
        return render_template("book.html", data = None)

if __name__ == "__main__":
    app.run(debug=True)