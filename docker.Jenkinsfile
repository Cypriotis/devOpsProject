pipeline {

    agent any

    environment {
            DOCKER_TOKEN = credentials('docker-push-secret')
            DOCKER_USER = 'cypriotis'
            DOCKER_SERVER = 'ghcr.io'
            DOCKER_PREFIX = 'ghcr.io/cypriotis/django'
        }

    stages {

        stage('Clone') {
            steps {
                git branch: 'main', url: 'git@github.com:Cypriotis/devopsproject.git'
            }
        }
    



        stage('docker build') {
            steps {
                sh '''
                    HEAD_COMMIT=$(git rev-parse --short HEAD)
                    TAG=$HEAD_COMMIT-$BUILD_ID
                    docker build --rm -t $DOCKER_PREFIX:$TAG -t $DOCKER_PREFIX:latest -f nrdjango.Dockerfile .
                '''
            }
        }

        stage('test') {
            steps {
                sh '''
                    HEAD_COMMIT=$(git rev-parse --short HEAD)
                    TAG=$HEAD_COMMIT-$BUILD_ID
                    cd devopsproject
                    cp devopsproject/.env.example devopsproject/.env
                    docker run --env-file ./devopsproject/.env $DOCKER_PREFIX:$TAG python manage.py test

                '''
            }
        }

        stage('push docker image') {
            steps {
                sh '''
                    HEAD_COMMIT=$(git rev-parse --short HEAD)
                    TAG=$HEAD_COMMIT-$BUILD_ID
                    cat $DOCKER_TOKEN
                    cat $DOCKER_TOKEN | docker login $DOCKER_SERVER -u $DOCKER_USER --password-stdin
                    docker push $DOCKER_PREFIX --all-tags

                '''
            }
        }

        stage('install docker to tagret vm') {
            steps {
                sh '''
                    ansible-galaxy install geerlingguy.docker
                    ansible-galaxy install geerlingguy.pip
                '''
                sh '''
                    ansible-playbook -i ~/workspace/ansible-project/hosts.yml -l deploy-vm-1 ~/workspace/ansible-project/playbooks/docker-install.yml

                '''
            }

        }
    }
}