# RevoBank Application API

## Overview
This API provides a comprehensive set of endpoints for managing users, accounts, and transactions in a banking application. Built using **uv** python package and project manager as well as **Flask** for the virtual environment. In addition, this API is Deployed on **Koyeb** for reliable cloud hosting. It supports user authentication, account management, and transaction processing. 

## Features Implemented
1. **User Management**:
   - Create a new user account.
   - Retrieve and update the profile of the currently logged-in user.

2. **Authentication**:
   - Login to an existing user account.

3. **Account Management**:
   - Retrieve a list of all accounts or details of a specific account.
   - Create, update, or delete an account.

4. **Transaction Management**:
   - Retrieve a list of all transactions or details of a specific transaction.
   - Initiate new transactions (deposit, withdrawal, or transfer).

## Installation and Setup

### Prerequisites
- uv installed

### Steps
1. Clone the repository:
   ```
   git clone https://github.com/your-repo/bank-app-api.git
   cd Revou-Module-7-Assignment
   ```

2. Install all dependencies:
   ```
   uv sync
   ```
   Kill and restart terminal to run the terminal using the virtual environment.

3. Run the application:
   ```
   uv run task fr
   ```

4. The API will be available at `http://127.0.0.1:3005`.
   
5. Run the tests:
   ```
   uv run pytest -v -s --cov=.
   ```

## API Usage Documentation

The full documentation of each endpoints, along with their request requirements and expected  response are shown in [API Documentation](https://vmh9e49dyw.apidog.io)

### Base URL
This API is deployed using **Koyeb**  with the following base url for the API request.
`mad-adriane-dhanapersonal-9be85724.koyeb.app/`

## Database Schema Documentation
<img src="https://github.com/DhanaNugraha/Revou-Module-7-Assignment/blob/main/assets/database-schema.png">


## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

---
## License

---

## Contact
For questions or support, please contact [dhananugraha1511@gmail.com](mailto:dhananugraha1511@gmail.com).


