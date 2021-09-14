# Planning Poker Server application

A Flask Application listening to socketio events to update/create the Planning Poker Game's state.
The ReactJS Client application of Planning Poker Game can be found here: https://github.com/Rudrarka/planning-poker-ui-ts

## Demo
A demo of the app can be seen here: https://epidemic-voting.netlify.app/
## Motivation

In order to estimate how complex a task is for a team of developers to complete, a common technique that is used is called "planning poker".

* Each developer gets to vote on a task by giving their estimate as a point.
* The set of points you can cast your vote on is usually a predefined set of arbitrary numbers, something like this: 0, 1/2, 1, 2, 3, 5, 8, 13.
* The higher the number, the more complex the task is to complete.

This application demonstrates the Planning poker application where the users can do the following:
* Create a poll. A user creates a poll and can share this link with other people.
* Join a pre-existing poll created by you or someone else. You should be able to cast your vote on different points in a predefined set (0, 1/2, 1, 2, 3, 5, 8, 13). A user can only vote once, but can change their vote.
* Visualize the results in real-time of a poll: Anyone should be able to see the results of a poll. If user A is casting a vote "2", user B should in real-time be able to see that the point "2" has a value of 1.

## Prerequisites

### Install Docker
Refer to https://docs.docker.com/get-docker/ to install docker

## Cloning and Running the Application in local

* Clone the project into local
    ```bash
    git clone
    ```

* Run the following commands to build and run the application:
    ```bash
    cd planning-poker-server
    docker build . -t planning-poker-server
    docker run -it -p 5000:5000 planning-poker-server
    ```


The Application Runs on **localhost:5000**
