### Server Functions for Wolf Team

1. Requirements
  - Python3
  - Screen GNU
  - Configure path to this scripts functions
  - Push 3 params to script `execute` like `./execute.sh 1 2 3`
    1: (1) Update core game and mods (2) Update only core game (3) Update only mods
    2: Steam user
    3: Steam pass
  - This script are fully compatibility with several instances of Arma game / users linux
  - If a mod download fails it will retry to download (typical error in steamcmd when mods are heavy) 
  > But you will have to configure and modify some things commented in the scripts
  - Enjoy!

2. Advices
  - Create an alias with user and pass to each action
  - Place files on /opt/update_arma
  - The script will generate a file `update.log` with a log of the application
  - Care, `execute.sh` does not run the script on background, if you use CTRL+C, you will broke the process
  - You can create a cronjob which execute this script every day
