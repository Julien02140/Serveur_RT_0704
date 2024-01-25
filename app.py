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
        g.id = session["id"]

@app.route("/supprime_session")
def supprime_session():
    session.pop("utilisateur", None)
    session.pop("id", None)
    flash("Vous êtes deconnecté","success")
    return render_template("login.html")

@app.route("/home") #home page de l'application
def home():
    api_populaire = API_URL + "films_populaires"
    if g.utilisateur:
        response = requests.get(api_populaire)
        if response.status_code == 200:
            listes_films = []
            for film in response.json():
                listes_films.append(film)
            return render_template("home.html",utilisateur=session["utilisateur"],id=session["id"],films_populaires=listes_films)
    return redirect(url_for("run"))

@app.route('/description/<int:film_id>')
def description_film(film_id):
    api_description = API_URL + f"trouver_film/{film_id}"
    response = requests.get(api_description)
    if response.status_code == 200:
        film = response.json()
        print("poster_path",film['poster_path'])
        return render_template("description_film.html",film=film)

@app.route('/videotheque/<int:id>')
def get_videotheque(id):
    api_videotheque = API_URL + f"ma_videotheque/{id}"
    reponse1 = requests.get(api_videotheque)
    liste_films = []
    if reponse1.status_code == 200:
        liste_films_id = reponse1.json()["liste_films"]
        print("voici les id : ",liste_films_id)
        for film_id in liste_films_id:
            print("film_id", film_id)
            api_trouver_film = API_URL + f"trouver_film/{film_id}"
            reponse2 = requests.get(api_trouver_film)
            if reponse2.status_code == 200:
                liste_films.append(reponse2.json())
                print("Film ajouté à la liste")
            else:
                print("film introuvable")
        return render_template("videotheque.html",films=liste_films) 
    else:
      return "Echec de la requete"

@app.route("/page_register")
def page_register():
    return render_template('register.html')

@app.route("/register", methods=['POST'])
def register():
    session.pop("utilisateur",None)
    session.pop("id",None)
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
    session.pop("id",None)
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
            session["id"] = reponse.json().get("id")
            #url_for retourne sur la fonction qui s'appelle home, pas la route
            return redirect(url_for("home"))
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
    
@app.route("/supprimer_film/<int:film_id>")
def supprimer_film(film_id):
    print("SUPPRIME LE FILM")
    user_id = session["id"]
    api_supprimer_film = API_URL + f"supprimer_film/{user_id}/{film_id}"
    reponse = requests.get(api_supprimer_film)
    if reponse.status_code == 200:
        flash("film supprimer",'success')
        return redirect(url_for("home"))



@app.route("/ajout_film/<int:film_id>")
def ajout_film(film_id):
    user_id = session["id"]
    api_trouver_film = API_URL + f"ajout_film/{user_id}/{film_id}"
    reponse = requests.get(api_trouver_film)
    if reponse.status_code == 200:
        if reponse.json().get("message") == "Deja dans la videotheque":
            print("film deja dans la videotheque")
            flash("film deja dans la videotheque",'success')
        else:
            print("film ajouté")
            flash("film ajouté",'success')         
    else:
        print("film introuvable")
        flash("film introuvable",'success')

    return redirect(url_for("home"))

@app.route("/recherche_film", methods = ['POST'])
def recherche_film():
    if request.method == 'POST':
        donne = request.form
        mot = donne.get("recherche")
        print("mot",mot)
        api_recherche_film = API_URL + f"recherche_film/{mot}"
        reponse = requests.get(api_recherche_film)
        if reponse.status_code == 200:
            liste_films = reponse.json().get("liste_films")
            return render_template("home.html",films_populaires=liste_films)
        else:
            return "erreur"

    
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int("3000"),debug=True)