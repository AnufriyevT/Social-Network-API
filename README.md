# Social Network API
## Test task

Clone this project

Add virtual environment

Install all requirements
```bash
    pip install -r requirements.txt
```

To run this project go into src dir

Run:
```bash
    python manage.py runserver
```
### Posts
You can go to http://127.0.0.1:8000/api/post/ to see posts

### Users
You can go to http://127.0.0.1:8000/api/users/ to see users

You can go to http://127.0.0.1:8000/api/users/1/ to see details of user with id=1 if such user exists in database
### Analytics
You can go to http://127.0.0.1:8000/api/analytics/ to see likes aggregated by day

User parameters pub_date__lte or pub_date__gte to filter likes

Example url: http://127.0.0.1:8000/api/analytics/?pub_date__lte=2021-02-21&pub_date__gte=2021-02-18

### Swagger
To see the whole scheme of API go to http://127.0.0.1:8000/api/redoc/