# Messenger [![CI/CD](https://github.com/VyacheslavShrot/messenger/actions/workflows/ci_cd.yml/badge.svg)](https://github.com/VyacheslavShrot/messenger/actions/workflows/ci_cd.yml)

- The part of the backend that describes the basic functionality of the messenger<br><br>
- I have described in detail how to use the APIs of this project in the <strong>Postman documentation</strong> :
    - <strong>https://documenter.getpostman.com/view/26500283/2s9Yyy9Jru </strong><br><br>
- Also in the image on my <strong>Docker Hub</strong> is always the latest version of the code using the <strong>GitHub CD</strong> :
    - <strong>https://hub.docker.com/r/vyacheslavshrot/messenger </strong>

# Structure

- This project is written in the latest version of <strong>Python 3.11</strong> along with the <strong>FastAPI</strong> framework<br><br>

- <strong>All code</strong> is <strong>asynchronous</strong> like my previous projects<br><br>

- <strong>NoSQL</strong> database <strong>MongoDB</strong> is connected via official images<br><br>

- Written easy <strong>PyTest</strong> tests for a simple notion that everything is working properly<br><br>

- <strong>CI/CD actions</strong> on pull request:
    - <strong>CI</strong>:
        - the same <strong>PyTest</strong> tests are used<br><br>
    - <strong>CD</strong>:
        - <strong>pushing</strong> an image to my <strong>Docker Hub</strong><br><br>

- There are 2 main kinds of <strong>APIs</strong> here:
    - For <strong>User</strong>:
        - APIs for <strong>registration</strong> and <strong>login</strong> with obtaining <strong>JWT token</strong> for user <strong>
          authorization</strong><br><br>

    - For <strong>Messages</strong>:
        - APIs for <strong>creating chat</strong>, <strong>get messages</strong>, and <strong>sending messages</strong>
            - <strong>aiocache</strong> is also used to <strong>record</strong> and if available, <strong>take messages</strong> from
              the <strong>cache</strong><br><br>
            - <strong>WebSocket</strong> is used to implement chat functionality<br><br>

- Also added a <strong>manifest</strong> for <strong>kubernetes</strong> (which I will still improve)

# Launch in Docker-Compose

- You need to create an <strong>.env file</strong> at the <strong>docker-compose file level</strong> and write the variables<br><br>

- For this purpose, a ready-made Docker-Compose file has already been built using:
    - image <strong>vyacheslavshrot/messenger:latest</strong>:
        - for this container, write a <strong>SECRET_KEY</strong> variable for the <strong>JWT token</strong> ( it can be a random
          value )<br><br>

    - image <strong>mongo</strong>:
        - for this container we write:
            - <strong>MONGO_INITDB_ROOT_USERNAME</strong><br><br>
            - <strong>MONGO_INITDB_ROOT_PASSWORD</strong><br><br>
            - <strong>MONGO_DB_AUTH_SOURCE</strong> ( for this variable usually <strong>admin</strong> value is used)<br><br>

    - image <strong>mongo-express</strong>:
        - <strong>ME_CONFIG_MONGODB_ADMINUSERNAME</strong> ( use the same data as for image mongo )<br><br>
        - <strong>ME_CONFIG_MONGODB_ADMINPASSWORD</strong> ( use the same data as for image mongo )<br><br>
        - <strong>ME_CONFIG_MONGODB_SERVER=mongo</strong><br><br>

- After installing the environment, we run <strong>docker-compose up -d</strong><br><br>

- Go to the <strong>mongo-admin panel</strong> ( mongo-express container ):
    - Create the base <strong>messenger</strong><br><br>
  
    - Create 3 <strong>collections</strong>:
      - <strong>users</strong><br><br>
      
      - <strong>chat</strong><br><br>
      
      - <strong>messages</strong><br><br>

- And at the level of docker-compose.yml create a folder <strong>mongodb_data</strong> where our data from the database will be stored