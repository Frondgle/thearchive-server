# The Sonatore Archive Server

In loving memory of emosurrealist Alex Cheng. Emosurrealism lives on. ♡

### [client-side code](https://github.com/Frondgle/thearchive-client)

### Tech and Frameworks Used

<div align="center">  
<a href="https://www.python.org/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/python-original.svg" alt="Python" height="50" /></a>  
<a href="https://www.djangoproject.com/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/django-original.svg" alt="Django" height="50" /></a>  
<a href="https://www.postgresql.org/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/postgresql-original-wordmark.svg" alt="PostgreSQL" height="50" /></a>
<a href ="https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white"><img style="margin:10px" src="https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white" /></a>  
</div>

* Also, shout out to Cloudinary

#### Concept and Aesthetic driven by
* Daley 
* Jorge

### Dev Contributors:
* [A.J. Gonzalez](https://github.com/gonzalez-aj)
* [Eric L Frey](https://github.com/ericlfrey)
* [Charles Bridgers IV](https://github.com/SeaForeEx)

## First Time Setup

If you don't have a virtual environment set up yet:

- Create a virtual environment:
```bash
   python3 -m venv venv
```

- Activate the virtual environment:
```bash
   source venv/bin/activate
```

- Install dependencies:
```bash
   pip install -r requirements.txt
```

- Run migrations:
```bash
   python3 manage.py migrate
```

- Run the server:
```bash
   python3 manage.py runserver
```

#### Steps to run the Python Server
- Activate the virtual environment:
```bash
   source venv/bin/activate
```

- Run the Django development server:
```bash
   python3 manage.py runserver
```

- Access the application: Open your browser to `http://localhost:8000`

- To deactivate the virtual environment when done:
```bash
   deactivate
```

#### Steps to deploy changes
- git checkout -b branch-name
- make changes to branch-name
- git add .
- git commit -m "message"
- git push origin branch-name
- cmd click GitHub link
- bypass rules and merge (for now)
- git checkout main
- git pull origin main
- git fetch origin deploy (if you don't have deploy branch yet)
- git checkout deploy
- git merge main
- git push origin deploy
- **If you changed models:** run `heroku run python manage.py migrate` to apply database changes

#### Important Notes
- **Always run migrations on Heroku after changing models** - Your local migrations won't automatically apply to production
- To verify migrations worked: `heroku run python manage.py showmigrations`