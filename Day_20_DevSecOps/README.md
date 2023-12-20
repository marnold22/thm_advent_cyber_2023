# Day_20 [DevSecOps] Advent of Frostlings

+ Deployable Machine: Yes
+ GITLABS: Yes
  + UN: DelfSecOps
  + PW: TryHackMe!

Description: One of the main reasons the Best Festival Company acquired AntarctiCrafts was their excellent automation for building, wrapping, and crafting. Their new automation pipelines make it a much easier, faster, scalable, and effective process. However, someone has tampered with the source control system, and something weird is happening! It's suspected that McGreedy has impersonated some accounts or teamed up with rogue Frostlings. Who knows what will happen if a malicious user gains access to the pipeline? In this task, you will explore the concept of poisoned pipeline execution (PPE) in a GitLab CI/CD environment and learn how to protect against it. You will be tasked with identifying and mitigating a potential PPE attack. A GitLab instance for AntarctiCrafts' CI/CD automates everything from sending signals and processing Best Festival Company services to building and updating software. However, someone has tampered with the configuration files, and the logs show unusual behaviour. Some suspect the Frostlings have bypassed and gained access to our build processes.

> IP: [10.10.171.232]

## LEARNING OBJECTIVES

1. Learn about poisoned pipeline execution.
2. Understand how to secure CI/CD pipelines.
3. Get an introduction to secure software development lifecycles (SSDLC) & DevSecOps.
4. Learn about CI/CD best practices.

## OVERVIEW

1. Important components of GitLabs
   1. Version control system: A VCS is the environment where you manage and track changes made in the codebase. It makes it easier to collaborate with others and maintain the history and versioning of a project.
   2. CI/CD pipelines: Pipelines automate the building, testing, and deployment processes. Pipelines ensure the code is consistently integrated, tested, and delivered to the specified environment (production or staging).
   3. Security scanning: GitLab has a few scanning features, like incorporating static application security testing (SAST), dynamic application security testing (DAST), container scanning, and dependency scanning. All these tools help identify and mitigate security threats in code and infrastructure.
2. CI/CD
   1. **Continuous integration**: CI refers to integrating code changes from multiple contributors into a shared repository (where code is stored in a VCS; you can think of it as a folder structure). In GitLab, CI allows developers and engineers to commit code frequently, triggering automations that lead to builds and tests. This is what CI is all about: ensuring that code changes and updates are continuously validated, which reduces the likelihood of vulnerabilities when introducing security scans and tests as part of the validation process (here, we start entering the remit of DevSecOps).
   2. **Continuous deployment**: CD automates code deployment to different environments. During SDLC, code travels to environments like sandbox and staging, where the tests and validations are performed before they go into the production environment. The production environment is where the final version of an app or service lives, which is what we, as users, tend to see. CD pipelines ensure the code is securely deployed consistently and as part of DevSecOps. Integrating security checks before deployment to production is key.
3. CI/CD Attacks: PPE
   1. In today's AoC, you will learn about poisoned pipeline execution. This type of attack involves compromising a component or stage in the SDLC. For this attack to work, it takes advantage of the trust boundaries established within the supply chain, which is extremely common in CI/CD, where automation is everywhere.
   2. When an attacker has access to version control systems and can manipulate the build process by injecting malicious code into the pipeline, they don't need access to the build environment. This is where the "poisoned" pipelines come into play. It's crucial to have effective, secure gates and guardrails to prevent malicious code from getting far if there is an account compromise.

## STEPS

1. Deploy Machine
2. Navigate to website
   1. Sign into gitlabs
   2. Go to the Advent-Calendar-BFC repository dashboard
3. GITLABS
   1. Lets look at the YAML config file

      ```yaml
         workflow:
         rules:
            - if: $CI_COMMIT_BRANCH

         install_dependencies:
         stage: build
         script:
            - echo "This is the installation step"

         before_script:
         - |
            # Check if docker is running then terminate to free port
            CONTAINER_NAME="affectionate_saha"
            if docker ps -a --format "{{.Names}}" | grep -q "^$CONTAINER_NAME$"; then
               echo "Stopping existing container..."
               docker stop $CONTAINER_NAME
               docker rm $CONTAINER_NAME
            fi

         test:
         stage: test
         script:
            - whoami
            - pwd
            - ls -la    
            - ls -la ./public/
            - echo "Testing some Christmas things yes, yes..."
            - >
               echo "<html><head><title>Advent of Cyber Calendar</title><style>* {margin: 0;padding: 0;}.imgbox {display: grid;height: 100%;}.center-fit {max-width: 100%;max-height: 100vh;margin: auto;}</style></head>
               <body><div class='imgbox'><img class='center-fit'src='images/Day_20_defaced_calendar.png' alt='Advent Calendar BFC'></div></body></html>" > ./public/index.html
            
            - docker run -d --name $CONTAINER_NAME -v $(pwd)/public/:/usr/local/apache2/htdocs/ -p 9081:80 httpd:latest
         artifacts:
            paths:
               - public/
         rules:
            - if: $CI_COMMIT_BRANCH == "main"
      ```

      1. In here we see the main components and rules
      2. Specifically we see the docker commands and the port that it will be served on = `9081`
      3. And it is using `apache` as the serving platform
4. INVESTIGATION
   1. Lets look at the Merge Requests
      1. Click on the "Merged" tab
         1. In here we see the commits made to the code
            1. Specifically we see changes in the yaml

               ```yaml
                  rules:
                     - if: $CI_COMMIT_BRANCH == "main"
                     - if: $CI_COMMIT_BRANCH != "main"
               ```

            2. We also see an PNG that was changed to a "DEFACED_CAL.png" where it displays `Frostlings Rule`
         2. In the "OVERVIEW" tab we see
            1. Frostlino `@BadSecOps` approved this merge request
5. PIPELINE LOGS
   1. Click CI/CD -> Jobs
      1. In here we can see ecah individual pipeline view
6. COMMIT HISTORY
   1. Click Repository -> Commits
   2. Scrolling through we can see the original commit by Delf Lead
      1. Commit `986b7407` by Delf Lead -> "Adding test deploy pipeline for calendar"
7. FIX
   1. Now lets copy the original code and restore it
   2. Click "View File" and copy the original code
   3. Navigate back to config.yaml file
   4. Edit -> Edit in Pipeline Panel
      1. Copy original code
      2. Commit!

## QUESTIONS

1. What is the handle of the developer responsible for the merge changes?
   1. `@BadSecOps`
2. What port is the defaced calendar site server running on?
   1. `9081`
3. What server is the malicious server running on?
   1. `apache`
4. What message did the Frostlings leave on the defaced site?
   1. `Frostlings Rule`
5. What is the commit ID of the original code for the Advent Calendar site?
   1. `986b7407`