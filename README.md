<img src="assets\Github Readme.png" />

<hr/>

# Comms

### Cloning the repository

### Clone the repository using the command below :
```bash
git clone https://github.com/arindam-sahoo/Community-WebApp.git
```

### Create a virtual environment :
```bash
# create a virtual environment
python -m venv .venv

# activate our virtual environment
.\.venv\Scripts\activate
```

### Install the requirements :
```bash
pip install -r requirements.txt
```

### Move into the directory where we have the project files : 
```bash
cd backend
```

#

### Running the App

### We need to create a self server database :
```bash
python manage.py makemigrations
python manage.py migrate
```

### To run the App, we use :
```bash
python manage.py runserver
```

> ⚠ Then, the development server will be started at http://127.0.0.1:8000/