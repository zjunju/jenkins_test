pipeline {
    agent {
        docker {image 'python:3.5.1'}
    }
    stages {
        stage('build') {
            steps {
                sh 'python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/'
                sh 'python -m pip install --upgrade setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple/'
                sh 'python -m pip install -r requirments.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ '
                sh 'python manage.py runserver 0.0.0.0:25557'
            }
        }
    }
}
