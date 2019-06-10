#!groovy​

pipeline {
    agent any
    environment {
        AWS_ACCESS_KEY_ID     = credentials('jenkins-aws-secret-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('jenkins-aws-secret-access-key')
        FOO = "FOO"
    }
    stages {
        stage ('Checkout') {
            steps {
                checkout scm
            }
        }
        stage ('Setup') {
            steps {
                sh 'python3 --version'
                echo 'Configure virtualenv'
                VENV_PATH = 'Envs/deploy'
                sh 'virtualenv ${WORKSPACE}/${VENV_PATH}'
                sh '${WORKSPACE}/$VENV_PATH}/bin/pip install -r ${WORKSPACE}/deploy/requirements.txt'
            }
        }
        stage ('Deploy') {
            steps {
                echo 'Deploying application'
            }
        }
        stage ('Test') {
            steps {
                echo 'Running tests'
            }
        }
    }
}