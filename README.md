# Amity_Room_Allocation
 A python algorithm to automatically assign rooms to people added to the system.
<img width="807" alt="screen shot 2017-01-04 at 12 32 35" src="https://cloud.githubusercontent.com/assets/23119824/21637892/0907056a-d27a-11e6-98ea-8248cbcf56d7.png">

## Installation
Clone the repo on github using the link
`git@github.com:ianoti/Amity_Room_Allocation.git`

navigate to the folder

`Amity_Room_Allocation`

and fetch the develop branch by running

`git pull origin develop`

set up the virtual environment and install dependencies by running.
`pip install -r requirements.txt`

## Running the program
From the command line execute the command.
`python run.py -i`

## Tests
To run tests cd to the `Amity_Room_Allocation` folder and run the command.

`nosetests --with-coverage --cover-erase`

## Usage
The interface shows the commands used in the program as well as the correct syntax for usage.

The commands that have an option of output to file store the outputs in the `data\` folder of the application.

All database files created are located in the `Amity_Room_Allocation` root folder.
