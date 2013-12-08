import os

PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print PROJECT_DIR
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'bitvid.db'),
    }
}

try:
	from awsinfo import AWS_ACCESSAWS_SECRET
except:
	AWS_ACCESS = ''
	AWS_SECRET = ''