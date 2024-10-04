
# Ryan Connect

Ryan Connect is a web application designed to help immigrants connect with each other.

## Setup Instructions

### Prerequisites

- Python 3.6 or higher
- Git

### Installation

1. **Clone the Repository**

   Open your terminal and clone the repository using the following command:

   ```bash
   git clone https://github.com/Migration-Network/Ryan-Connect.git
   cd ryan-connect
   ```

2. **Create and Activate a Virtual Environment**

   Create a virtual environment for the project:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install Dependencies**

   Install the required packages using the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   The `.env` file is already included in the project and should contain the following content:

   ```env
   FLASK_ENV=development
   FLASK_DEBUG=1
   ```

5. **Initialize the Database**

   Run the following commands to set up the database:

   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the Application**

   Start the development server:

   ```bash
   flask run
   ```

   The application will be available at `http://127.0.0.1:5000`.

### Additional Notes

- Ensure the `countries+states+cities.json` file is in the `app/static/js/` directory for location data.
- The `site.db` SQLite database file will be created in the `instance/` folder upon initialization.
