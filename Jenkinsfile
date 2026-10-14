
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        DOCKER_IMAGE = 'bettaiebtraining/microapp'
    }

    stages {

        stage('Charger .env') {
            steps {
                script {
                    def envFile = '.env'

                    if (!fileExists(envFile)) {
                        error("Fichier .env introuvable à la racine du dépôt.")
                    }

                    def config = [:]

                    readFile(envFile).split('\n').each { line ->
                        line = line.trim()

                        if (line && !line.startsWith('#') && line.contains('=')) {
                            def parts = line.split('=', 2)
                            config[parts[0].trim()] = parts[1].trim()
                        }
                    }

                    ['APP_NAME', 'APP_PORT', 'APP_VERSION'].each { key ->
                        if (!config[key]) {
                            error("Variable ${key} absente ou vide dans .env")
                        }
                        env[key] = config[key]
                    }

                    echo "Application : ${env.APP_NAME}"
                    echo "Port        : ${env.APP_PORT}"
                    echo "Version     : ${env.APP_VERSION}"
                    echo "Branche     : ${env.BRANCH_NAME ?: 'non définie'}"
                }
            }
        }

        stage('Build Docker') {
            steps {
                sh '''
                    set -eu

                    echo "Construction de l'image Docker..."
                    echo "Application : $APP_NAME"
                    echo "Version : $APP_VERSION"

                    docker build \
                      --build-arg APP_NAME="$APP_NAME" \
                      --build-arg APP_PORT="$APP_PORT" \
                      -t "$DOCKER_IMAGE:$APP_VERSION" \
                      -t "$DOCKER_IMAGE:latest" \
                      .
                '''
            }
        }

        stage('Test Docker') {
            steps {
                sh '''
                    set -eu

                    echo "Vérification de l'image..."
                    docker image inspect "$DOCKER_IMAGE:$APP_VERSION"

                    echo "Image construite avec succès."
                '''
            }
        }

        stage('Login Docker Hub') {
            when {
                branch 'main'
            }
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        set +x
                        echo "$DOCKER_PASSWORD" | docker login \
                          --username "$DOCKER_USER" \
                          --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    set -eu

                    docker push "$DOCKER_IMAGE:$APP_VERSION"
                    docker push "$DOCKER_IMAGE:latest"
                '''
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo 'Étape de déploiement à configurer selon le serveur cible.'
                echo "Image prête : ${env.DOCKER_IMAGE}:${env.APP_VERSION}"
            }
        }
    }

    post {
        success {
            echo "Pipeline terminé avec succès pour ${env.BRANCH_NAME ?: 'branche inconnue'}."
        }

        failure {
            echo 'Pipeline en échec : consulter les logs.'
        }

        always {
            echo 'Fin du pipeline.'
        }
    }
}
