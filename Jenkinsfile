pipeline{
    agent any
     environment {
        EC2_HOST = "ec2-user@13.233.150.180"
        PRIVATE_KEY = credentials('ec2-creds')
        DOCKER_USER = "chinmaykulkarni19"
        DOCKER_PASS = credentials('docker-hub-creds') 
    }

    stages{
        stage('Checkout code'){
            steps{
                 git branch: 'main', url: 'https://github.com/chinmaykul-1/whiskerwagg-backend'
            }
        }
        stage('Logon to aws node and pull image'){
            steps{
                withCredentials([sshUserPrivateKey(credentialsId: 'ec2-creds', keyFileVariable: 'SSH_KEY'),
                usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')])
                {
                    sh """
                    ssh -i $SSH_KEY $EC2_HOST << 'EOF'
                    echo "connected to ec2 node"
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    docker pull chinmaykulkarni19/whiskerwagg-backend
                    docker stop backend  || true
                    docker rm backend || true
                    docker run -p 8000:8000 --rm --name backend chinmaykulkarni19/whiskerwagg-backend
                    'EOF'
                    """
                }

            }
        }

    }
}