pipeline {
    agent {
        docker {image 'python:3.5.1'}
    }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
                sh 'python -m pip install -r requirments.txt'
            }
        }
    }
}
