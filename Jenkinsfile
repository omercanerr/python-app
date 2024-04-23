pipeline {
  agent any
    environment {
        APP_NAME = "${APP_NAME}"
        NAMESPACE = "${NAMESPACE}"
        KUBECONFIGID= "${KUBECONFIGID}"
    }
options { timestamps () }
stages { 
    stage('Cloning Git') {
      steps {
        git([url: 'https://github.com/omercanerr/python-app.git', branch:'main'])
      }
    }
   stage('Sonarqube') {
node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    def scannerHome = tool 'SonarScanner';
    withSonarQubeEnv() {
      sh "${scannerHome}/bin/sonar-scanner"
    }
  }
}
    }
}
    stage('Building image') {
      steps{
        script {
            dockerImage = docker.build("${APP_NAME}-${NAMESPACE}:${env.BUILD_ID}", "--no-cache -f Dockerfile .")    
        }
      }
    }
    stage('Pushing Image') {
      steps{
        script {
          docker.withRegistry( 'http://172.31.211.70:8083/docker/', 'docker-credentials' ) {
            dockerImage.push("${env.BUILD_ID}")
          }
        }
      }
    }
    stage('Clean Up') {
        steps {
            script {
                try{
                    sh 'docker image rm ${APP_NAME}-${NAMESPACE}:${BUILD_ID}'
                    sh 'docker image rm 172.31.211.70:8083/${APP_NAME}-${NAMESPACE}:${BUILD_ID}'
                }
                catch(err){}
            }
        }
    }
}
}
