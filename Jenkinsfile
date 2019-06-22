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
                slackSend message: "Build Started - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
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
                sshagent(['b12f5eac-0b8c-4bae-844c-b4275a8cf4b6']) {
                    echo 'Deploying application'
                    sh '${WORKSPACE}/${DEPLOY_VENV_PATH}/bin/python ${WORKSPACE}/deploy_django.py'

                    sh 'git tag -a v_${BUILD_NUMBER}b -m "Jenking Build #${BUILD_NUMBER}"'
                    sh 'git push origin --tags'
                }
            }
        }
        stage ('Test') {
            steps {
                echo 'Running tests'
                slackSend color: 'good', message: "Complete - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
            }
        }
    }
}

def notifyBuild(String buildStatus = 'STARTED') {
  // build status of null means successful
  buildStatus =  buildStatus ?: 'SUCCESSFUL'

  // Default values
  def colorName = 'RED'
  def colorCode = '#FF0000'
  def subject = "${buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
  def summary = "${subject} (${env.BUILD_URL})"
  def details = """<p>STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
    <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>"""

  // Override default values based on build status
  if (buildStatus == 'STARTED') {
    color = 'YELLOW'
    colorCode = '#FFFF00'
  } else if (buildStatus == 'SUCCESSFUL') {
    color = 'GREEN'
    colorCode = '#00FF00'
  } else {
    color = 'RED'
    colorCode = '#FF0000'
  }

  // Send notifications
  slackSend (color: colorCode, message: summary)
}