pipeline {
    agent any
    stages {
        stage('Cancel previous build if any') {
            steps {
                cancelPreviousBuilds()
            }
        }
        stage('Push to Dev Repository') {
            steps {
                sh 'sh "../../../Infrastructure Team Pipeline/repository/push.sh" --repository=repo-1 --environment=dev'
            }
        }

        stage('Integ Compile') {
            steps {
                sh 'sh "../../../Infrastructure Team Pipeline/lambda/compile.sh" --repository=repo-1 --environment=integ'
            }
        }

        stage('Integ Tests') {
            steps {
                sh 'sh "../../../Infrastructure Team Pipeline/lambda/test.sh" --repository=repo-1 --environment=integ'
            }
        }

        stage('Generate / Apply Migration Script for Integ') {
            steps {
                script {
                    sh 'python3.8 -m pip install -r requirements_dev.txt'
                    sh 'cd DatabaseModels && python3.8 -m pip install -r requirements.txt'
                    sh 'export AWS_PROFILE=terraform-integ && cd DatabaseModels && python3.8 manage.py migrate'
                }
            }
        }

        stage('Deploy to Integ Jenkins') {
            steps {
                sh 'sh "../../../Infrastructure Team Pipeline/lambda/upload.sh" --repository=repo-1 --environment=integ'
                // sh 'mvn -f "../../../Infrastructure Team Pipeline/pom.xml" -pl InfrastructureJobs exec:java -Dexec.mainClass="com.partsavatar.infrastructure.jobs.JobsBootstrap" -Dstage=terraform-integ -Dexec.args="-job=API_SYNC -aws-account=626555359476 -environment=integ -repository=repo-1" -Dhibernate.skip.schema.validation=true'
                sh 'mvn -f "../../../Infrastructure Team Pipeline/pom.xml" -pl InfrastructureJobs exec:java -Dexec.mainClass="com.partsavatar.infrastructure.jobs.JobsBootstrap" -Dstage=terraform-integ -Dexec.args="-job=LAMBDA_JOB_SYNC -aws-account=626555359476 -repository=repo-1" -Dhibernate.skip.schema.validation=true'
            }
        }

        stage('Deploy to Production?') {
            steps {
                script {
                    timeout(time: 1, unit: 'DAYS') {
                        input(message: 'Deploy to Production?')
                    }
                }
            }
        }

         stage('Push to Prod Repository') {
            steps {
                sh 'sh "../../../Infrastructure Team Pipeline/repository/push.sh" --repository=repo-1 --environment=prod'
            }
        }

        stage('Prod Compile') {
            steps {
                sh 'sh "../../../Infrastructure Team Pipeline/lambda/compile.sh" --repository=repo-1 --environment=prod'
            }
        }

        stage('Prod Test') {
            steps {
                sh 'sh "../../../Infrastructure Team Pipeline/lambda/test.sh" --repository=repo-1 --environment=prod'
            }
        }

        stage('Generate / Apply Migration Script for Production') {
            steps {
                script {
                    sh 'export AWS_PROFILE=terraform-prod && cd DatabaseModels && python3.8 manage.py migrate'
                }
            }
        }

        stage('Deploy to Prod Jenkins and reload config') {
            steps {
                sh 'sh "../../../Infrastructure Team Pipeline/lambda/upload.sh" --repository=repo-1 --environment=prod'
                // sh 'mvn -f "../../../Infrastructure Team Pipeline/pom.xml" -pl InfrastructureJobs exec:java -Dexec.mainClass="com.partsavatar.infrastructure.jobs.JobsBootstrap" -Dstage=terraform-prod -Dexec.args="-job=API_SYNC -aws-account=975964192410 -environment=prod -repository=repo-1" -Dhibernate.skip.schema.validation=true'
                sh 'mvn -f "../../../Infrastructure Team Pipeline/pom.xml" -pl InfrastructureJobs exec:java -Dexec.mainClass="com.partsavatar.infrastructure.jobs.JobsBootstrap" -Dstage=terraform-prod -Dexec.args="-job=LAMBDA_JOB_SYNC -aws-account=975964192410 -repository=repo-1" -Dhibernate.skip.schema.validation=true'
                sh 'java -Dstage=prod -Dhibernate.skip.schema.validation=true -jar /data/jobs/InfrastructureJobs.jar -job=PATH_SYNC_JOB -source-path=JenkinsJob -destination-path=/home/ubuntu/new-jenkins/jenkins-efs-mount-point/jobs/Products-team/jobs/repo-1/'
                sh 'java -jar /data/jobs/jenkins-cli.jar -s https://jenkins.partsavatar.ca/ -webSocket groovy = < /data/jobs/reload-jenkins-configuration.groovy'
            }
        }
    }
    post {
        success {
            echo "BUILD SUCCESS"
        }
        failure {
            echo "BUILD FAILURE"
        }
    }
}

def cancelPreviousBuilds() {
    def hudson = Hudson.instance
    def pname = env.JOB_NAME.split('/')[0]
    def jobName = env.JOB_NAME
    def buildNumber = env.BUILD_NUMBER.toInteger()
    def currentJob = Jenkins.instance.getItemByFullName(jobName)

    for (def build : currentJob.builds) {
        if (build.isBuilding() && build.number.toInteger() != buildNumber && build.number.toInteger() < buildNumber) {
            build.doStop()
        }
    }
}
