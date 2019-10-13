pipeline {
    agent {
        docker {image 'python:3.5.1'}
    }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
                sh 'python -m pip list'
                sh 'python -m pip install --upgrade pip'
                sh 'python -m pip install --upgrade setuptools'
                sh 'python -m pip install -r requirments.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ ' 
            }
        }
    }
}
