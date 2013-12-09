BitVid
======


Installation
============

Download and set up the repository
```
/ >virtualenv BitVid
/ >cd BitVid
/BitVid > git clone https://github.com/CrateMuncher/BitVid.git
/BitVid >cd BitVid

Linux:
/BitVid/BitVid > source bin/activate
Windows: 
/BitVid/BitVid > Scripts\activate.bat
/BitVid/BitVid > pip install requirements.txt
```

Setup the Database
```
/BitVid/BitVid > python manage.py syncdb
/BitVid/BitVid > python mnage.py migrate
```

Setup the Search
================

Download elasticsearch(elasticsearch.com) and run it with its default configuration:
```
./bin/elasticsearch
```

Index the Data
```
python manage.py rebuild_index 
```


And you're ready to go:
```
/BitVid/BitVid > python manage.py runserver
```
