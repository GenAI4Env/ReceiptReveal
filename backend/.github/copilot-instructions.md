# Copilot Instructions

## Poetry Configuration

```toml
[project]
name = "carbon-scanner"
version = "0.0.0"
description = "This is the backend code for Carbon Scanner, a web app that analyzes product carbon emissions."
authors = [
    {name = "GenAI4Env", email = "GenAI4Env/CarbonScanner@simplelogin.com"}
]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.11,<4.0"
dependencies = [
    "openai (>=1.68.2,<2.0.0)",
    "cohere (>=5.14.0,<6.0.0)",
    "google-genai (>=1.7.0,<2.0.0)",
    "aiohttp (>=3.11.14,<4.0.0)",
    "flask[async] (>=3.1.0,<4.0.0)",
    "aiosqlite (>=0.21.0,<0.22.0)"
]

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
package-mode = false
```

### Important Notes for Copilot

1. The project should use Python 3.11.x or above (but below 4.0).  
2. Dependencies are managed with [Poetry](https://python-poetry.org/)—ensure that any new dependency is added to `pyproject.toml` instead of a separate requirements file.  
3. The code is structured with separate modules for functionalities like authentication, database interactions, generative AI integrations, etc.

---

## Project Structure

The project is organized into the following directories and files:

```text
carbon-scanner/
├── authentication/
├── database/
├── genai/
├── tests/
├── poetry.lock
├── pyproject.toml
└── README.md
```

Below is an overview of each directory and file:

### 1. authentication/

- Manages user authentication and authorization logic.
- Expected to contain functions/classes for handling user credentials, tokens, permission checks, etc.

### 2. database/

- Manages database connections, migrations, and queries.
- Contains scripts, models, or any utility to handle data persistence (possibly using SQLite and “aiosqlite”).

### 3. genai/

- Houses features and utilities that use generative AI (OpenAI, Cohere, Google GenAI).
- Contains request handlers, configuration setups, and custom logic for generative AI calls.

### 4. tests/

- Contains unit, integration, or end-to-end tests.
- Organize tests by module to keep coverage clear.

### 5. poetry.lock

- Auto-generated file that ensures consistent dependency versions across environments.

### 6. pyproject.toml

- Main configuration file for Poetry.
- Defines project metadata, dependencies, and tool settings.

### 7. README.md

- High-level documentation for the project.
- Includes instructions for local setup, purpose, usage examples, and contribution guidelines.

---

## Usage Instructions

1. Clone this repository locally.  
2. Install and configure [Poetry](https://python-poetry.org/docs/).  
3. From the project root, run:  

   ```bash
   poetry install
   ```

   This installs all dependencies listed in `pyproject.toml`.  

4. Activate the virtual environment using:  

   ```bash
   poetry shell
   ```

5. Run or develop the application (e.g., using Flask or an async approach) within this environment.  

---

## Contribution Guidelines for Copilot

1. Maintain folder structure, keeping all authentication-related code in the “authentication” directory, database interactions in the “database” directory, and AI logic in “genai” directory.  
2. For new features, create a separate module or subfolder if appropriate.  
3. Update or create tests in the “tests” directory.  
4. Ensure all code snippets and examples align with dependencies specified in `pyproject.toml`.  
5. When scaffolding new code, keep Python versions, dependencies, and project requirements in mind.  
