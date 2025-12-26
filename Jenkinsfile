pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
    }

    stages {

        stage("Setup Python Env") {
            steps {
                sh """
                python3 -m venv ${VENV_DIR}
                source ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage("Ingestion") {
            steps {
                sh "source ${VENV_DIR}/bin/activate && scripts/run_ingestion.sh"
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
