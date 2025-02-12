# Lottery System

The Trufin Lottery System is a Python-based application that selects and stores 25 unique winners from different America States using an external API. The system ensures that only one winner per state is stored at a time, and the data is saved in a PostgreSQL database.

## Project Structure

```tree
├── Makefile                       # Defines commands for starting the app and running tests
├── app                            # Main application directory
│   ├── api                        # Handles external API requests
│   │   └── fetch_random_users.py  # Fetches random users from the API
│   ├── db                         # Database connection management
│   │   └── db_connection.py       # Manages PostgreSQL connections
│   ├── repositories               # Handles database interactions
│   │   └── winner_repository.py   # Manages winner storage and retrieval
│   ├── services                   # Business logic layer
│   │   ├── lottery_service.py     # Runs the lottery process
│   │   └── user_service.py        # Manages user-related operations
│   └── utils                      # Utility functions and configurations
│       ├── config.py              # Loads environment variables
│       ├── constants.py           # Defines global constants
│       └── logger.py              # Manages logging functionality
├── main.py                        # Entry point for running the application
├── tests                          # Contains unit tests
│   └── test_lottery_system.py     # Tests lottery system functionality
├── pyproject.toml                 # Dependency and configuration management
└── uv.lock                        # Dependency lock file
```

## Getting Started

### Prerequisites

To run this application, you need the following installed on your system:

- Python 3.12 or higher
- PostgreSQL
- `uv` package manager

### Installation

Clone the repository and install the required dependencies:

```bash
git clone http://github.com/ahmedali8/trufin-lottery-system
cd trufin-lottery-system
```

### Environment Variables

Create a `.env` file in the project root by copying [.env.example](.env.example) file

```bash
cp .env.example .env
```

### Running the Application

Start the lottery process with the following command:

```bash
uv run main.py
```

or use `Makefile`:

```base
make start
```

### Running Tests

To verify that the system is working correctly, run the unit tests:

```bash
PYTHONPATH=. uv run python -m unittest discover tests
```

or use `Makefile`:

```base
make test
```

## Features

- Fetches random users from an external API
- Stores unique winners with only one per state
- Saves data in PostgreSQL for persistence
- Uses structured logging for better debugging
- Includes unit tests to ensure reliability
- Provides a Makefile for easier command execution
