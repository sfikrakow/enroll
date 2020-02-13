# SFI workshop enroll

## Quick development setup
```shell script
git clone https://git.sfi.pl/scm/we/enroll.git
cd enroll
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
