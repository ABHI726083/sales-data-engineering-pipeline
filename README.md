name: CI



on:

&#x20; push:

&#x20;   branches:

&#x20;     - main

&#x20; pull\_request:

&#x20;   branches:

&#x20;     - main



jobs:

&#x20; test:



&#x20;   runs-on: ubuntu-latest



&#x20;   steps:



&#x20;     - name: Checkout repository

&#x20;       uses: actions/checkout@v4



&#x20;     - name: Set up Python

&#x20;       uses: actions/setup-python@v5

&#x20;       with:

&#x20;         python-version: "3.14"



&#x20;     - name: Install dependencies

&#x20;       run: |

&#x20;         python -m pip install --upgrade pip

&#x20;         pip install -r requirements.txt



&#x20;     - name: Run tests

&#x20;       run: |

&#x20;         pytest -v

