from flask import Flask, render_template
helloworld = Flask(__name__)
@helloworld.route("/")
def run():
    return render_template('index.html')

@helloworld.route("/login")
def login():
    return render_template('login.html')

@helloworld.route("/register")
def register():
    return render_template('register.html')

if __name__ == "__main__":
    helloworld.run(host="0.0.0.0",port=int("3000"),debug=True)