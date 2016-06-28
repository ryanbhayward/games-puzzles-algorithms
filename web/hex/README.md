# CMPUT 396 - Hex Web Interface

A minimal web interface for hex game agents.

## Installation

### Prerequisites

- A Python3 interpreter
- [`bower`](https://bower.io/)
    - To install `bower`: `npm install -g bower` (Requires [`npm`](https://www.npmjs.com/))
        - To install `npm`:
            - Ubuntu/Debian: `apt-get install npm`
            - OSX: `brew install npm` (Requires [`homebrew`](http://brew.sh/))
            - Fedora: `dnf install npm`
            - Arch: `pacman -S npm`
            - openSUSE: `zypper install npm`
- `make` (Optional)
- `venv` (Optional)

### Procedure

#### With `make`

- Simply call `make install` to handle installing needed dependencies with
  `make`.

#### Without `make`

- Install python dependencies by running `pip install -r requirements.txt`.
- Install javascript dependencies by running `bower install`.

## Running

- Run the web server by running `python3 application.py`.
- Note the address and port the web server displays on startup (e.g. http://127.0.0.1:5000/), and open this in a web browser.
