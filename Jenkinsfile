pipeline {
    agent any
    environment {
        IMAGE_TAG = "latest"
        IMAGE_REPO_NAME = "omercaner/python-app"
        REPOSITORY_URI = "docker.io/${IMAGE_REPO_NAME}:${IMAGE_TAG}"
        DOCKER_BINARY = "/usr/bin/docker"
        SONARQUBE_URL = "http://192.168.0.35:9000"
        SONARQUBE_LOGIN = "jenkins"
    }

    stages {
       
        stage('Cloning git') {
            steps {
                script {
                    git branch: 'main', url: 'https://github.com/omercanerr/python-app.git'
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
        
        stage ('Running SonarQube analysis') {
            steps {
                script {
                    withSonarQubeEnv('sonar') {
                        sh "sonarqube \
                            -Dsonar.projectKey=python \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=${SONARQUBE_URL} \
                            -Dsonar.login=${SONARQUBE_LOGIN}"
                    }
                }
            }  
              
              
        
        stage ('Pushing to DockerHub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub_credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                        sh "${DOCKER_BINARY} push ${REPOSITORY_URI}"
                    }
                }
            }
        }
        
    }
}
