// Jenkinsfile

pipeline {
    agent any

    parameters {
        string(
            name: 'BASE_URL',
            defaultValue: 'https://fakerestapi.azurewebsites.net',
            description: 'API base URL'
        )
    }

    environment {
        // Make BASE_URL available to the tests
        BASE_URL   = "${params.BASE_URL}"
        REPORT_DIR = "reports"
        REPORT_FILE = "report.html"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip
                    pip3 install -r book-store-api-tests/requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                    mkdir -p ${REPORT_DIR}
                    # This env var can be used by tests if needed
                    export BASE_URL=${BASE_URL}

                    python3 -m pytest book-store-api-tests/tests \
                        --html=${REPORT_DIR}/${REPORT_FILE} \
                        --self-contained-html \
                        --log-cli-level=INFO
                '''
            }
        }
    }

    post {
        always {
            // Archive the HTML report as a build artifact
            archiveArtifacts artifacts: "${REPORT_DIR}/**", fingerprint: true

            // Publish the Pytest HTML report in Jenkins
            publishHTML(target: [
                reportName: 'Pytest Report',
                reportDir: "${REPORT_DIR}",
                reportFiles: "${REPORT_FILE}",
                keepAll: true,
                alwaysLinkToLastBuild: true
            ])
        }
    }
}
