# Private-Console-Communicator
Encryption-protected console messaging app

# Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)

# Introduction
This is a simple console messaging app that allows you to send messages to other user. The messages are encrypted on the client side, so the server cannot read them. The server only stores the encrypted messages and sends them to the recipient. The recipient then decrypts the message on their side.

# Prerequisites
- [Python 3.6+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installing/)

# Installation
1. Clone the repository
```
git clone https://github.com/NaviteLogger/Private-Console-Communicator.git
```

(Optional) Create a virtual environment
```
python -m venv venv
```

2. Install the required packages
```
pip install -r requirements.txt
```

# Usage
1. Start the server (server.py file located under the server folder)
```
python server.py
```

2. Start the client (app.py file located under the client folder)
```
python client.py
```
