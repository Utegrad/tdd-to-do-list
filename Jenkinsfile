#!groovy​

pipeline {
    agent any
    environment {
        AWS_ACCESS_KEY_ID     = credentials('jenkins-aws-secret-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('jenkins-aws-secret-access-key')
        APP_SECRETS_NAME = credentials('beta-secrets-name')
        SSH_USERNAME = credentials('beta-host-server-ssh-username')
        SSH_PASSWORD = credentials('beta-host-server-ssh-password')
        SSH_HOST     = credentials('beta-host-server-ssh-host')
        REGION_NAME = 'us-east-1'
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
                sh 'git tag -a v_${BUILD_NUMBER} -m "Jenking Build #${BUILD_NUMBER}"'
                sh 'git push origin --tags'
                echo 'Deploying application'
                sh '${WORKSPACE}/${DEPLOY_VENV_PATH}/bin/python ${WORKSPACE}/deploy/deploy.py'
            }
        }
        stage ('Test') {
            steps {
                echo 'Running tests'
            }
        }
    }
}