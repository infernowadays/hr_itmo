# Project HR ITMO backend

Server part of the website by:
- Searching for startups for students all over the world;
- Telegram bot to notify students about new projects suitable for their specialization;
- Convenient and native system of skills and search for the necessary projects.

## Demo
Web client: http://findfound.me/

## Built with
- [Django](https://www.djangoproject.com/) - a free framework for web applications in Python
- [DRF](https://www.django-rest-framework.org/) - a library that works with standard Django models to create flexible and powerful API
- [Telegram Bot Api](https://core.telegram.org/bots/api) - api from the Telegram messenger to create chat bots

## Installation
<i> For questions: [@infernowadays](https://t.me/infernowadays "@infernowadays") </i>
- Install postgres and configure in
- `backend/settings.py`
- Open a command line window and go to the project's directory.
- `sudo apt-get install build-essential libssl-dev libffi-dev python3-dev python-dev`
- `pip install -r requirements.txt`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver` or `python manage.py runserver 0.0.0.0:<your_port>`

## Todo
- [X] Useful metrics
- [ ] Atomicity of existence
- [ ] Distribution to the largest universities in the Russian Federation
- [ ] Worldwide distribution
- [ ] Spread across the galaxy
- [X] And many more interesting things!
