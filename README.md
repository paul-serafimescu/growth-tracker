# growth-tracker

## Setup

### Prerequisites
[Node.js](https://nodejs.org/en/) and [Python 3.9+](https://www.python.org/)

### Instructions

**note: this assumes some understanding of how to set up a Discord API application**
- create a discord application
    - specifically a bot scope
- create a `.env` file in the root directory to house all your credentials
    - example as follows:
    ```bash
    BOT_CLIENT_TOKEN=<Your bot token>
    SECRET_KEY=<Django secret key>
    CLIENT_SECRET=<Discord application secret>
    CLIENT_ID=<Discord application client id>
    ```
- install dependencies
    - Python (pip) `pip -r requirements.txt`
    - Node.js (npm) `cd frontend && npm install`

### Cleaning Up
theoretically `make clean` should remove all binary files and migrations but I'm not sure if this is a smart idea

### Issues
lol

<br/>
<br/>

<sub><sup>this project isn't done yet</sup></sub>
