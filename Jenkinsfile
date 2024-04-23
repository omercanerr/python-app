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
    steps {
        withSonarQubeEnv('sonar') {
            sh '''${scannerHome}/sonar-scanner-5.0.1.3006/bin/sonar-scanner \
            -Dsonar.sources=${WORKSPACE} \
            -Dsonar.projectBaseDir=${WORKSPACE} \
            -Dsonar.projectKey=${SONARPROJECTKEY} \
            -Dsonar.projectName=${SONARPROJECTKEY} \
            -Dsonar.sourceEncoding=UTF-8 \
            -Dsonar.working.directory=${WORKSPACE}/sonar \
            -X
            '''
        }
//         timeout(time: 1, unit: 'HOURS') {
//           waitForQualityGate abortPipeline: true,
//           credentialsId: 'sonartoken'
//         }
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
