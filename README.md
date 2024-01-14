### Steps to run the project.

**Create a virtual environment**
```bash
python3 -m venv venv
```

**Initialize virtual environment**

For linux
```
source venv/bin/activate
```

For Windows
```powershell
venv\Scripts\Activate
```

**Move inside the folder**
```bash
cd lesson025
```

**Download the requirements**
```bash
pip install -r requirements.txt
```

**Move inside the folder**
```bash
cd address_book
```

**Make migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Run the project**
```bash
python manage.py runserver
```