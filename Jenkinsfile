pipeline {
    agent any

    stages {
        stage('Checkout - Serveur') {
            steps {
                // Checkout principal (déjà automatique si Jenkinsfile dans ce repo)
                git url: 'https://github.com/Julien02140/Serveur_RT_0704.git', branch: 'main'
            }
        }

        stage('Checkout - API') {
            steps {
                dir('api') { // On met l'API dans un sous-dossier pour pas écraser le serveur
                    git url: 'https://github.com/Julien02140/Api_RT_0704.git', branch: 'main'
                }
            }
        }

        stage('Build Serveur') {
            steps {
                sh 'echo Build du Serveur...'
                // Commandes de build du Serveur ici
            }
        }

        stage('Build API') {
            steps {
                dir('api') {
                    sh 'echo Build de l\'API...'
                    // Commandes de build de l’API ici
                }
            }
        }

        stage('Déploiement') {
            steps {
                sh 'echo Déploiement en cours...'
                // Commandes de déploiement pour Serveur + API
            }
        }
    }
}
