#!groovy​

pipeline {
    agent any
    environment {
        AWS_ACCESS_KEY_ID     = credentials('jenkins-aws-secret-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('jenkins-aws-secret-access-key')
    }
    stages {
        stage ('Checkout') {
            steps {
                checkout scm
            }
        }
        stage ('Build') {
            steps {
                echo 'Configure virtualenv'
                echo "${AWS_ACCESS_KEY_ID}"
                sh 'python --version'
                sh 'python3 --version'
            }
        }
        stage ('Test') {
            steps {
                echo 'Running tests'
            }
        }
    }
}