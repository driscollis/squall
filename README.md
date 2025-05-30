# Squall SQLite Editor

Squall is a SQLite viewer and editor that runs in your terminal. Squall is written in Python and uses the [Textual package](https://github.com/Textualize/)

## Screenshots

Here is what Squall looks like using the [Chinook database](https://github.com/lerocha/chinook-database):

![squall_demo](https://github.com/user-attachments/assets/ecac6ac3-4d42-4d3d-9c15-2e129102a087)

## Command-Line Options

Currently, there is only one command-line option: `-f` or `--filename`, which allows you to pass a database path to Squall to load.

Example Usage:

`squall -f path/to/database.sqlite`

## Prerequisites

The instructions assume you have uv or pip installed.

## Installation

### PyPi

`uv tool install squall_sql`

### Using uv on GitHub

`uv tool install git+https://github.com/driscollis/squall`

## Update the Installation

If you want to upgrade to the latest version of Squall SQL, then you will want to run one of the following commands.

### Using uv on GitHub

`uv tool install git+https://github.com/driscollis/squall -U --force`

## Installing Using pip

`pip install squall-sql`

## Running Squall from Source

If you cloned the package and want to run Squall, one way to do that is to navigate to the cloned repo on your hard drive using your Terminal. Then run the following command while inside the `src` folder:

`python -m squall.squall`

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/driscollis/squall/blob/main/LICENSE) file for details.
