# MyCLIApp

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

Orme is a command-line interface (CLI) application that is in its early stages of development, it is intended to keep track of personal expenses and debts, in order to be able to have insights about personal financial situation such as, how much is the user expending in different time frames (weeks, months, years), what are the things in which the user expends more its money (food, bills, clothes, etc), as well as what debts the user has, or which of them the user is actually the lender.

Orme is currently changing and the objective is to add graphical information through several charts which help the user have a better view of all the information related to expenses, debts and investments.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

### Prerequisites

- Python 3.x

### Installation Steps

1. Create a virtual environment (optional but recommended since it is an alpha version):

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. Install the app directly from TestPyPI:

    ```sh
    pip install --extra-index-url https://testpypi.python.org/pypi orme=={version} # Current tested version 0.1.2.10
    ```

## Usage

Orme has 2 types of registers to be added and both of them have different arguments and options, you can always use the --help option to get information for each command.

### Registers

- expenses
- debts

### Examples

To register an expense you can use the following command:

```sh
    orme expenses add -- value 5000 --description 'Grosery store expense' --category 'food' --date '2024-06-11'
