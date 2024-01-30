# HRMS Staff System

## Steps to Launch the App

1. **Install Pip Packages:**
   - Open a terminal and navigate to the project directory.
   - Run the following command to install the required packages from `requirements.txt`:

     ```bash
     pip install -r requirements.txt
     ```

2. **Set Up Environment Variables:**
   - Locate the `.env.example` file in the project directory.
   - Rename the file to `.env`.
   - Open the `.env` file and fill out the following information:
     - `DATABASE_URL`: MySQL connection URL for your database.
     - `DEBUG`: Set to either `1` for debug mode or `0` for non-debug mode.
     - An example is already prefilled with a connection string for a database hosted on a student's server.
     - Note: If you prefer, you can host your database using the provided dump in `uweresto.sql`.

3. **Run the App:**
   - In the terminal, run the following command to start the app:

     ```bash
     python start.py
     ```

   - This will launch the application, and you should see relevant output indicating that the app is running.

4. **User Credentials:**
   - For a list of available users and their credentials, refer to the [CREDENTIALS.md](CREDENTIALS.md) file.

**Note:** The provided database will be kept working until the coursework is marked.
