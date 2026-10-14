pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo '🛠️ Build en cours...'
                sh 'mvn clean compile'
            }
        }
        stage('Test') {
            steps {
                echo '✅ Tests unitaires...'
                sh 'mvn test'
            }
        }
    }
}