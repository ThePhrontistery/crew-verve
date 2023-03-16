# Crew-verve - The Return of the Angry COBOL Mob

Crew-verve is a Python web app (built on [Flask](https://flask.palletsprojects.com/)) for measuring the mood of a team (or any other group of people for that matter). 
Crew-verve serves as a simple demo and playground for [Flask](https://flask.palletsprojects.com/), [Htmx](https://htmx.org/) and [Tailwind CSS](https://tailwindcss.com/).

## Installation

Clone the repository. Use the dependency and package manager [Poetry](https://python-poetry.org/) to install all the dependencies of Crew-verve.

```bash
poetry install
```

## Usage
[Activate the Python virtual environment](https://python-poetry.org/docs/basic-usage/#activating-the-virtual-environment) with

```bash
poetry shell
```
Run the Flask webserver with

```bash
flask run
```

or in debug-mode with:

```bash
flask --debug run
```

It will run by default on port 8080.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Copyright and license

Copyright © 2023 Iwan van der Kleijn

Licensed under the MIT License 
[MIT](https://choosealicense.com/licenses/mit/)