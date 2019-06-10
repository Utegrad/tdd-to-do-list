#!groovy​

pipeline {
    agent any
    environment {
        AWS_ACCESS_KEY_ID     = credentials('jenkins-aws-secret-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('jenkins-aws-secret-access-key')
        DEPLOY_VENV_PATH = 'Envs/deploy'
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
                sh 'virtualenv ${WORKSPACE}/${DEPLOY_VENV_PATH}'
                sh '${WORKSPACE}/${DEPLOY_VENV_PATH}/bin/pip install -r ${WORKSPACE}/deploy/requirements.txt'
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