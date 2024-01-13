from flask import Flask, render_template, request, jsonify
import requests
API_URL = "http://localhost:5000/api/"

helloworld = Flask(__name__)
@helloworld.route("/")
def run():
    return render_template('index.html')

@helloworld.route("/page_login")
def page_login():
    return render_template('login.html')

@helloworld.route("/page_register")
def page_register():
    return render_template('register.html')

@helloworld.route("/verif_login", methods=['POST'])
def verif_login():
    #recuperation des donnee de la requete post, c est en json.
    donnee = request.form
    print(donnee)
    reponse = requests.post(API_URL + "verif_user",donnee)
    if reponse.status_code == 200:
        reponse_api = reponse.json().get("message")
        if reponse_api == "Connexion OK":
            #recuperation un à un
            pseudo = donnee.get("username")
            password = donnee.get("password")
            return "bienvenu " + pseudo
        else:
            return "pseudo ou mot de passe faux"
    else:
        return "Echec de la requete vers l'api"

    # Faites une requête à l'API pour qu'elle verifie si le peudo et le mdp est correct
    """
    response = requests.get(API_URL + "verif_user")
    if response.status_code == 200:
        verif = response.txt
        if verif == "OK":
            return """



if __name__ == "__main__":
    helloworld.run(host="0.0.0.0",port=int("3000"),debug=True)