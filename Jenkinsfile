pipeline {
    agent any
    tools {
        maven 'maven3'
    }
    stages {
        stage('Build') {
            steps {
                echo '🛠️ Build en cours...'
                dir('demo-app') {
                    sh 'mvn clean compile'
        }
                
            }
        }
        stage('Test') {
            steps {
                echo '✅ Tests unitaires...'
                dir('demo-app') {
                    sh 'mvn test'
        }
            }
        }
    }
}