# SDCCProject
![parking now logo](https://github.com/Alefanfi/SDCCProject/blob/master/ClientWindows/gui/logo.png?raw=true)

## Requirements
This project uses docker and docker-compose to simulate the fog nodes locally.
Please refer to this links:
* [docker download](https://www.docker.com/products/docker-desktop)
* [docker compose download](https://docs.docker.com/compose/install/)

## Fog nodes
To create the fog nodes you need to run the following command from the terminal:
    
    docker-compose up --scale fognode=3

This will create both the proxy server, which redirects the client requests to one of the nodes, and the fog cluster.
You need to specify the number of instances of fognode you wish to create (in the above example we
used 3). 

[docker-compose up manual](https://docs.docker.com/compose/reference/up/)

#### Sensors
To simulate the sensors you can use the code provided in sensor.py. Just run the following command:

    python sensor.py
    
## Client
There are two client applications respectively for:
* Windows
* Mac

To use it just cd into the directory of your choice and run:
    
    python client.py

The gui shows if the parking spots are currently empty or not. To see the statistics just push the "show statistics" button.