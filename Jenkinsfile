#!groovy​

pipeline {
    agent any
    stages {
        stage ('Checkout') {
            steps {
                checkout scm
            }
        }
        stage ('Build') {
            steps {
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