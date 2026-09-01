pipeline {
    agent any
    environment {
        Docker_Tag = "v${BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'git-credentials', url: 'https://github.com/myfirstgitravindra/eks-cicd-project'
            }
        }
         stage('Dockerbuild') {
             steps {
                 sh "docker build -t 603401240749.dkr.ecr.us-east-1.amazonaws.com/eks-cicd-app:${Docker_Tag} ./app"
             }
         }
         stage('ECRlogin') {
             steps {
                 sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 603401240749.dkr.ecr.us-east-1.amazonaws.com'
             }
         }
         stage('Trivyscan') {
             steps {
                 sh "trivy image --severity HIGH,CRITICAL --exit-code 0 603401240749.dkr.ecr.us-east-1.amazonaws.com/eks-cicd-app:${Docker_Tag}"
             }
         }
         stage('PushtoECR') {
             steps {
                sh "docker push 603401240749.dkr.ecr.us-east-1.amazonaws.com/eks-cicd-app:${Docker_Tag}"
             }
         }
         stage('Updateconfig') {
             steps {
                 sh "aws eks update-kubeconfig --region us-east-1 --name cicd-demo-cluster"
             }
         }
         stage('Deploy to EKS') {
             steps {
                 // ADD THIS LINE: It replaces the broken image URL with your actual versioned build tag
                 sh "sed -i 's|image: .*|image: 603401240749.dkr.ecr.us-east-1.amazonaws.com/eks-cicd-app:${Docker_Tag}|g' k8s/deployment.yaml"
                 
                 sh "kubectl apply -f k8s/deployment.yaml"
                 sh "kubectl apply -f k8s/service.yaml"
                 sh "kubectl rollout status deployment/eks-cicd-app"
             }
         }
    }
}
