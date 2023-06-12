pipeline {
    agent any


    stages {
        stage('Build') {
            steps {
                // Get some code from a GitHub repository
                git branch: 'main', url: 'git@github.com:Cypriotis/devopsproject.git'

                
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    python3 -m venv myvenv
                    pwd
                    source /var/lib/jenkins/workspace/django-pipeline/myvenv/bin/activate
                    pwd
                    pip install -r requirements.txt
                    cd devopsproject
                    cp devopsproject/.env.example devopsproject/.env'''
            }
        }
        
    }
}