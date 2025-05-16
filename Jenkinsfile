pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Récupérer le code depuis ton dépôt Git
                git 'https://github.com/Julien02140/Serveur_RT_0704.git'
            }
        }

        stage('Build') {
            steps {
                // Exemple de build avec Maven
                sh "'/usr/share/maven/bin/mvn' clean install"
            }
        }

        stage('Test') {
            steps {
                // Exemple de test
                echo 'Exécution des tests ici'
            }
        }

        stage('Deploy') {
            steps {
                // Exemple de déploiement
                echo 'Déploiement sur le serveur'
            }
        }
    }
}
