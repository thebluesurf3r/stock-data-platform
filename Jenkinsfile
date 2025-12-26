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


        stage("Ingestion") {
            steps {
                sh '''
                ./venv/bin/python -m src.ingestion.ingest_job --symbol INFY --input_path data/sample_stock_data.csv
                '''
            }
        }

        stage("Processing") {
            steps {
                sh "source ${VENV_DIR}/bin/activate && scripts/run_processing.sh"
            }
        }

        stage("Indicators") {
            steps {
                sh "source ${VENV_DIR}/bin/activate && scripts/run_indicators.sh"
            }
        }

        stage("Model Training") {
            steps {
                sh "source ${VENV_DIR}/bin/activate && scripts/run_training.sh"
            }
        }

        stage("Smoke Tests") {
            steps {
                sh "source ${VENV_DIR}/bin/activate && scripts/smoke_tests.sh"
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
