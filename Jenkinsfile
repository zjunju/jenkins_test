pipeline {
    agent {
        docker {image 'python:3.5.1'}
    }
    stages {
        stage('build') {
            steps {
                sh 'ls -al '
               # sh 'python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/'
               # sh 'python -m pip install --upgrade setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple/'
               # sh 'python -m pip install -r requirments.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ ' 
               # sh '. restart.sh'
            }
        }
    }
}
