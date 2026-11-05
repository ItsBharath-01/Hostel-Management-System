pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    mkdir -p reports
                    .venv/bin/python -m pytest -v \
                    --junitxml=reports/test-results.xml \
                    | tee reports/test-results.txt
                '''
            }
        }

        stage('Build Artifact') {
            steps {
                sh '''
                    tar -czf hostel-management-build.tar.gz \
                    app tests run.py requirements.txt
                '''
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'hostel-management-build.tar.gz,reports/*',
                                 fingerprint: true
            }
        }
    }
}
