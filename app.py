from flask import Flask, render_template, request, jsonify, session, url_for, redirect,g, flash
import requests
import os
API_URL = "http://localhost:5000/api/"

app = Flask(__name__)
app.secret_key = os.urandom(24)
@app.route("/")
def run():
    return render_template('index.html')

@app.route("/page_login", methods=["GET","POST"])
def page_login():      
    return render_template('login.html')

@app.before_request #cela pemert à la fonction dessous d'être appelé quand il y a une requête
def avant_requete():
    g.utilisateur = None
    if "utilisateur" in session:
        g.utilisateur = session["utilisateur"]

@app.route("/supprime_session")
def supprime_session():
    session.pop("utilisateur", None)
    flash("Vous êtes deconnecté","success")
    return render_template("login.html")

@app.route("/account")
def account():
    if g.utilisateur:
        return render_template("account.html",utilisateur=session["utilisateur"])
    return redirect(url_for("run"))



@app.route("/page_register")
def page_register():
    return render_template('register.html')

@app.route("/register", methods=['POST'])
def register():
    session.pop("utilisateur",None)
    #recuperation des donnee de la requete post, c est en json.
    donnee = request.form
    #verification des champs, si ils sont vides
    for champ, valeur in donnee.items():
        if valeur.strip() == "":
            return "Un champ est vide"
    #On regarde aussi la confirmation du mot de passe
    password = donnee.get("password")
    confirm_password = donnee.get("confirm_password")
    if password != confirm_password:
        return "le mot de passe de confirmation n'est pas le même"
    
    reponse = requests.post(API_URL + "register_user",donnee)
    if reponse.status_code == 200:
        reponse_api = reponse.json().get("message")
        if(reponse_api == "Utilisateur ajouté"): 
            flash("compte cree",'success')
            return redirect(url_for("page_login"))
        else:
            return "problème sur l'api"
    else:
      return "Echec de l'inscription, problème de connexion"

@app.route("/verif_login", methods=['POST'])
def verif_login():
    session.pop("utilisateur",None)
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
            #cela supprime la session actuelle
            session["utilisateur"] = pseudo
            #url_for retourne sur la fonction qui s'appelle account, pas la route
            return redirect(url_for("account"))
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
    app.run(host="0.0.0.0",port=int("3000"),debug=True)