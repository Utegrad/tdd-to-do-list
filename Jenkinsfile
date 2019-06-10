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
                sh 'virtualenv ${WORKSPACE}/Envs/deploy'
                sh 'source ${WORKSPACE}/Envs/deploy/bin/activate'
                sh 'pip install -r ${WORKSPACE}/deploy/requirements.txt'
            }
        }
        stage ('Build') {
            steps {

            }
        }
        stage ('Test') {
            steps {
                echo 'Running tests'
            }
        }
    }
}