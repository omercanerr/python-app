pipeline {
    agent any
    environment {
        IMAGE_TAG = "latest"
        IMAGE_REPO_NAME = "omercaner/python-app"
        REPOSITORY_URI = "docker.io/${IMAGE_REPO_NAME}:${IMAGE_TAG}"
        DOCKER_BINARY = "/usr/bin/docker"
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
                    sh "${DOCKER_BINARY} build -t ${REPOSITORY_URI} ."
                }
            }
        }
        
        stage ('Pushing to DockerHub') {
            steps {
                script {
                    docker.withRegistry('', 'dockerhub_credentials') {
                        sh "${DOCKER_BINARY} push ${REPOSITORY_URI}"
                    }
                }
            }
        }
        
    }
}
