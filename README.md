
# flask-pastebin

This is my first Flask project.
I wanted to do pastebin web application to learn about Python and Web Applications.
Technology I have used:
- Flask
- Flask-WTF for forms and validation
- Flask-SQLAlchemy for Database functionality
- Flask-Login for user authentication
- Pytest for testing
- Jinja2 + Boostrap 5 for Templates

While there are tests most of them are not working since
 I've implemented Flask-WTF and most of the data validation
  goes through forms, there are only some Unit tests lefts.


## Features

- Publish public or private pastebins
- Paste expiration
- User privalges to view/edit/delete his own pastebins
- Syntax highlighting
- View recently created public pastebins
- Fetch all data through simple API

  
## Screenshots

<img src="https://github.com/syqu22/flask-pastebin/blob/main/web/static/01.png" height=50% width=60%>
<img src="https://github.com/syqu22/flask-pastebin/blob/main/web/static/02.png" height=50% width=60%>
<img src="https://github.com/syqu22/flask-pastebin/blob/main/web/static/03.png" height=50% width=60%>
<img src="https://github.com/syqu22/flask-pastebin/blob/main/web/static/04.png" height=50% width=60%>

  
## Installation 

First clone the repository to use it localy:
```sh
$ git clone https://github.com/syqu22/flask-pastebin.git
```

Then install all required libraries  through:

```bash 
  pip install -r requirements.txt
```
There's already an user preloaded in database and you can access him  with:

Login: ```test``` 

Password: ```test123```

There's also a special url ```/admin``` 
thanks to Flask-Admin, where you can have access to database from the website
    
## API Reference

#### Get user

```http
  GET /api/users/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | **Required**. Id of user to fetch |

#### Get users

```http
  GET /api/users
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `page` | `int` | Used to paginate (one page returns maximum of 50 users)|


#### Get pastebins of user

```http
  GET /api/users/${id}/pastebins
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | **Required**. Id of user to fetch |

#### Get pastebin

```http
  GET /api/pastebins/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | **Required**. Id of pastebin to fetch |

#### Get pastebins

```http
  GET /api/pastebins
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | Used to paginate (one page returns maximum of 50 pastebins) |



  
