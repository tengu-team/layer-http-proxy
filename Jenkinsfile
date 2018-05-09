pipeline {
    agent {
        docker { image 'jujusolutions/charmbox' }
    }
    
    stages {
        stage('Build') {
            steps {
                echo 'Test'
                sh 'charm version'
            }
        }
    }
}
