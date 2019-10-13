pipeline {
    agent any 
    stages {
        stage('build') {
            steps {
                sh 'echo "Hellp World"'
                sh '''
                    echo "Multiline shell steps works too"
                    ls -alh
                '''
            }
        }
    }
}
