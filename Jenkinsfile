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
                    . ./myvenv/bin/activate
                    pip install -r requirements.txt
                    echo here
                    cd devopsproject
                    cp devopsproject/.env.example devopsproject/.env'''
            }
        }
        
    }
}