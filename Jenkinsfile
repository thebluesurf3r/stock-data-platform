pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
    }

    stages {

        stage("Setup Python Env") {
            steps {
                sh '''
                python3 -m venv venv
                ./venv/bin/pip install --upgrade pip
                ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Generate Sample Data') {
            steps {
                sh '''
                mkdir -p data
                ./venv/bin/python src/utils/sample_data_generator.py \
                --output data/sample_stock_data.csv \
                --symbol INFY
                '''
            }
        }


        stage("Processing") {
            steps {
                sh '''
                scripts/run_processing.sh
                '''
            }
        }

        stage("Indicators") {
            steps {
                sh '''
                scripts/run_indicators.sh
                '''
            }
        }

        stage("Model Training") {
            steps {
                sh '''
                scripts/run_training.sh
                '''
            }
        }

        stage("Smoke Tests") {
            steps {
                sh '''
                scripts/smoke_tests.sh
                '''
            }
        }

    }

    post {
        failure {
            echo "❌ Pipeline failed"
        }
        success {
            echo "✅ Pipeline succeeded"
        }
    }
}
