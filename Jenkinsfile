pipeline {
    agent any
    environment {
        AWS_ACCOUNT_ID="****************"
        AWS_DEFAULT_REGION="US-EAST-2"
        IMAGE_REPO_NAME="cipipeline"
        IMAGE_TAG="latest"
        REPOSITORY_URI= "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}"
    }

    stages {
       
        stage('Cloning git') {
            steps {
                script {
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/omercanerr/python-app.git']])
                }
            }
        }
        
        stage ('Building Image') {
            steps {
                script {
                    dockerImage = docker.build "${IMAGE_REPO_NAME}:${IMAGE_TAG}"
                }
            }
        }
        stage ('Pushing to DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/omercaner/python-app', 'dockerhub_credentials') {
                    dockerImage.push("${IMAGE_REPO_NAME}:${IMAGE_TAG}")
                    }
                }
            }
        }
        
    }

}
