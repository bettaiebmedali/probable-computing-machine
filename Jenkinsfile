pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        stage('Charger .env') {
            steps {
                script {
                    if (!fileExists('.env')) {
                        error('Fichier .env introuvable à la racine du dépôt.')
                    }
                }

                sh '''
                    set -eu

                    # Lire les variables du fichier .env
                    APP_NAME=$(sed -n 's/^APP_NAME=//p' .env | head -n 1)
                    APP_PORT=$(sed -n 's/^APP_PORT=//p' .env | head -n 1)
                    APP_VERSION=$(sed -n 's/^APP_VERSION=//p' .env | head -n 1)

                    # Vérifier les valeurs
                    test -n "$APP_NAME" || {
                        echo "Erreur : APP_NAME absente de .env"
                        exit 1
                    }

                    test -n "$APP_PORT" || {
                        echo "Erreur : APP_PORT absente de .env"
                        exit 1
                    }

                    test -n "$APP_VERSION" || {
                        echo "Erreur : APP_VERSION absente de .env"
                        exit 1
                    }

                    # Enregistrer les variables pour les étapes suivantes
                    printf 'APP_NAME=%s\\nAPP_PORT=%s\\nAPP_VERSION=%s\\n' \
                        "$APP_NAME" "$APP_PORT" "$APP_VERSION" > .env.jenkins

                    echo "Application : $APP_NAME"
                    echo "Port        : $APP_PORT"
                    echo "Version     : $APP_VERSION"
                '''

                script {
                    def values = readFile('.env.jenkins').trim().split('\n')

                    env.APP_NAME = values[0].substring('APP_NAME='.length())
                    env.APP_PORT = values[1].substring('APP_PORT='.length())
                    env.APP_VERSION = values[2].substring('APP_VERSION='.length())
                }
            }
        }

        stage('Build Docker') {
            steps {
                sh '''
                    set -eu

                    echo "Construction de l'image..."
                    docker build \
                        --build-arg APP_NAME="$APP_NAME" \
                        --build-arg APP_PORT="$APP_PORT" \
                        -t "microapp:$APP_VERSION" \
                        -t "microapp:latest" \
                        .
                '''
            }
        }

        stage('Test Docker') {
            steps {
                sh '''
                    set -eu
                    docker image inspect "microapp:$APP_VERSION"
                    echo "Image Docker vérifiée."
                '''
            }
        }

        stage('Login Docker Hub') {
            when {
                branch 'main'
            }
            steps {
                echo 'Connexion Docker Hub à configurer si nécessaire.'
            }
        }

        stage('Push Docker') {
            when {
                branch 'main'
            }
            steps {
                echo 'Push à configurer après avoir défini le dépôt Docker Hub.'
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo "Déploiement à configurer pour ${env.APP_NAME}."
            }
        }
    }

    post {
        success {
            echo 'Pipeline terminé avec succès.'
        }
        failure {
            echo 'Pipeline en échec : consulter les logs.'
        }
        always {
            echo 'Fin du pipeline.'
        }
    }
}
