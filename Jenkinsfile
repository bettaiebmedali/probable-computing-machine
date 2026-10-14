pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'TON_DOCKERHUB_ID/microapp'
        APP_NAME = ''
        APP_PORT = ''
        APP_VERSION = ''
    }

    stages {
        stage('Charger .env') {
            steps {
                script {
                    if (!fileExists('.env')) {
                        error('Fichier .env introuvable')
                    }

                    def config = [:]

                    readFile('.env').split('\n').each { line ->
                        line = line.trim()

                        if (line && !line.startsWith('#')) {
                            def parts = line.split('=', 2)

                            if (parts.length == 2) {
                                config[parts[0].trim()] = parts[1].trim()
                            }
                        }
                    }

                    ['APP_NAME', 'APP_PORT', 'APP_VERSION'].each { key ->
                        if (!config[key]) {
                            error("Variable obligatoire absente : ${key}")
                        }
                    }

                    if (!(config.APP_PORT ==~ /[0-9]{1,5}/) ||
                        config.APP_PORT.toInteger() < 1 ||
                        config.APP_PORT.toInteger() > 65535) {
                        error('APP_PORT invalide')
                    }

                    if (!(config.APP_VERSION ==~ /[0-9A-Za-z][0-9A-Za-z_.-]*/)) {
                        error('APP_VERSION invalide')
                    }

                    env.APP_NAME = config.APP_NAME
                    env.APP_PORT = config.APP_PORT
                    env.APP_VERSION = config.APP_VERSION

                    echo "Application : ${env.APP_NAME}"
                    echo "Port : ${env.APP_PORT}"
                    echo "Version : ${env.APP_VERSION}"
                    echo "Branche : ${env.BRANCH_NAME}"
                }
            }
        }

        stage('Build Docker') {
            steps {
                sh '''
                    set -eu

                    docker build \
                        --build-arg APP_NAME="$APP_NAME" \
                        --build-arg APP_PORT="$APP_PORT" \
                        --build-arg APP_VERSION="$APP_VERSION" \
                        -t "$DOCKER_IMAGE:$APP_VERSION" \
                        .
                '''
            }
        }

        stage('Test Docker') {
            steps {
                sh '''
                    set -eu

                    docker run -d \
                        --name "microapp-test-${BUILD_NUMBER}" \
                        -p 127.0.0.1::8080 \
                        "$DOCKER_IMAGE:$APP_VERSION"

                    cleanup() {
                        docker rm -f "microapp-test-${BUILD_NUMBER}" >/dev/null 2>&1 || true
                    }
                    trap cleanup EXIT

                    PORT=$(docker port "microapp-test-${BUILD_NUMBER}" 8080/tcp | sed 's/.*://')

                    OK=0
                    for i in $(seq 1 20); do
                        if curl -fsS "http://127.0.0.1:$PORT/health" | grep -q healthy; then
                            OK=1
                            break
                        fi
                        sleep 1
                    done

                    test "$OK" -eq 1
                    curl -fsS "http://127.0.0.1:$PORT/"
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
                        printf '%s' "$DOCKER_PASSWORD" |
                            docker login -u "$DOCKER_USER" --password-stdin
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

                    docker tag "$DOCKER_IMAGE:$APP_VERSION" "$DOCKER_IMAGE:latest"
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
                echo "Déploiement prévu de ${env.DOCKER_IMAGE}:${env.APP_VERSION}"
                echo 'Étape de déploiement à configurer selon le serveur cible.'
            }
        }
    }

    post {
        always {
            echo "Fin du pipeline : ${env.BRANCH_NAME}"
        }
        success {
            echo 'Pipeline terminée avec succès.'
        }
        failure {
            echo 'Pipeline en échec : consulter les logs.'
        }
    }
}
