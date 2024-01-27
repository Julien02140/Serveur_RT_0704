from flask import Flask, render_template, request, jsonify, session, url_for, redirect,g, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
import os

#API_URL = "http://localhost:5000/api/"
API_URL = "http://api:5000/"

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
login_manager = LoginManager(app)

#modèle utilisateur
class User(UserMixin):
    def __init__(self, user_id,name,is_admin):
        self.id = user_id
        self.name = name
        self.is_admin = is_admin
    
    def get_id(self):
        return str(self.id)

#admin_user = User(0,"admin")

# Fonction de chargement de l'utilisateur pour Flask-Login
@login_manager.user_loader
def load_user(user_id):
     response = requests.get(API_URL + f"get_user/{user_id}")
     if response.status_code == 200:
        user_data = response.json()
        if user_data['id'] == 0:
            return User(user_data['id'], user_data['pseudo'],True)
        else:
            return User(user_data['id'], user_data['pseudo'],False)


@app.route('/page_admin')
@login_required
def admin_panel():
    if current_user.is_admin:
        return render_template('page_admin.html')
    else:
        return "page non autorisé"


@app.route("/")
def run():
    return render_template('index.html')

@app.route("/page_login", methods=["GET","POST"])
def page_login():      
    return render_template('login.html')

@app.route('/supprime_session')
@login_required
def supprime_session():
    logout_user()
    flash("Vous êtes déconnecté", "success")
    return render_template("index.html")


@app.route("/home") #home page de l'application
@login_required
def home():
    api_populaire = API_URL + "films_populaires" #les films populaires sont les premiers films dans films.json
    if current_user:
        response = requests.get(api_populaire)
        if response.status_code == 200:
            liste_films = []
            for film in response.json():
                liste_films.append(film)
            return render_template("home.html",films_populaires=liste_films)
    return redirect(url_for("run"))

@app.route('/description/<int:film_id>')
@login_required
def description_film(film_id):
    api_description = API_URL + f"trouver_film/{film_id}"
    response = requests.get(api_description)
    if response.status_code == 200:
        film = response.json()
        print("poster_path",film['poster_path'])
        return render_template("description_film.html",film=film)

@app.route('/videotheque/<int:id>')
@login_required
def videotheque(id):
    api_videotheque = API_URL + f"videotheque/{id}"
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
      return render_template("videotheque.html")
      

@app.route("/page_register")
def page_register():
    return render_template('register.html')

@app.route("/register", methods=['POST'])
def register():
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
            user_id = reponse.json().get("id")
            #creation du user
            if user_id == 0:
                user = User(user_id,pseudo,True)
            else:
                user = User(user_id,pseudo,False)
            login_user(user)
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
@login_required
def supprimer_film(film_id):
    print("SUPPRIME LE FILM")
    api_supprimer_film = API_URL + f"supprimer_film/{current_user.id}/{film_id}"
    reponse = requests.get(api_supprimer_film)
    if reponse.status_code == 200:
        flash("film supprimer",'success')
        return redirect(url_for("home"))



@app.route("/ajout_film/<int:film_id>")
@login_required
def ajout_film(film_id):
    user_id = current_user.get_id()
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
@login_required
def recherche_film():
    if request.method == 'POST':
        donne = request.form
        mot = donne.get("recherche")
        print("mot",mot)
        api_recherche_film = API_URL + f"recherche_film/{mot}"
        reponse = requests.get(api_recherche_film)
        liste_films = []
        if reponse.status_code == 200:
            liste_films = reponse.json().get("liste_films")
            print("liste des films :",liste_films)
            return render_template("recherche.html",films=liste_films)
        else:
            flash("ereur probleme de connexion",'success')
            return render_template("home.html",films=liste_films)
        
@app.route("/recherche_genre/<int:id>")
@login_required
def recherche_genre(id):
    api_recherche_genre = API_URL + f"recherche_genre/{id}"
    reponse = requests.get(api_recherche_genre)
    liste_films = []
    if reponse.status_code == 200:
        liste_films = reponse.json().get("message")
        print("liste des films :",liste_films)
        return render_template("recherche.html",films=liste_films)
    else:
        print("erreur de communication")
        return render_template("home.html",films=liste_films)

@app.route("/ajout_note",methods = ['POST'])
@login_required
def ajout_note():
    note = request.form.get('note')
    id_film = request.form.get('id')
    """api_trouver_film = API_URL + f"trouver_film/{id_film}"
    reponse_film = requests.get(api_trouver_film)
    if reponse_film.status_code == 200:
        film_note = reponse_film.json()"""
    #return f"Note : {note} pour le film : {id_film} pour l'utilisateur : {user_id}"
    api_note = API_URL + f"ajout_note/{current_user.id}/{id_film}/{note}"
    reponse = requests.get(api_note)
    if reponse.status_code == 200:
        message = reponse.json().get('message')
        film_note = reponse.json().get('film_note')
        if message == "Note ajoutée":
            flash("note ajouté","success")
            return render_template("description_film.html",film=film_note)
        elif message == "Note modifiée":
            flash("Note modifié","success")
            return render_template("description_film.html",film=film_note)
            #les messages flash ne fonctionne pas avec url_for, donc je suis
            #obligé de retrouver le film
            #return redirect(url_for('description_film',film_id=id_film))
        #flash("note ajouté","success")
        #return render_template("description_film.html",utilisateur=session["utilisateur"],id=session["id"],film=film_note)
    else:
        flash("probleme connexion, note non comptabilisé","success")
        return render_template("description_film.html",film=film_note)

    
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int("3000"),debug=True)