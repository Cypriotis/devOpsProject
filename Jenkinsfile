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
                    apt install python3.8-venv
                    python3 -m venv myvenv
                    source myvenv/bin/activate
                    pip install -r requirements.txt
                    cd devopsproject
                    cp devopsproject/.env.example devopsproject/.env'''
            }
        }
        
    }
}