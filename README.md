# elina

This is a fully fledge Django app which fetches alphavantage API every hour and gets BTC/USD exchange rate, 
and it stores into DB. Also, it provides three API endpoints for retrieving the data and fetching the rate at the moment.

**Tech Stack:**
Django, PostgreSQL, Redis, Celery, Nginx

**Setup:**
1- Obtain an API key from alphavantage change the .env.example to .env, and add your API key to that
also, if you want to enable the DEBUG in Django, you can set it in the .env file edit the Django secret key to your 
desire secret key. 

_Hint_
By default, it uses the 82 as TCP port for serving the data, and you can access the admin panel 
via 127.0.0.1:82/admin. If you want to deploy it on a domain due to using Django 4,
you have to change _CSRF_TRUSTED_ORIGINS_ in Django settings.


2- For spinning her up, you can start with this command:
`docker-compose up --build`
only for the first time; after that, you can remove the _--build_ switch.

**Using**

It provides five endpoints:

**_1-_** 
for obtaining an API key or token, you need to go one of these options:
**a.** (the easy option) send a post request to `/api/v1/create_api_key` with an optician JSON with a name like below :
`{ name: "test" }`
then it returns a JSON that contains the name and the API key like this :
`{ name: "test", key:"some_characters" }`
which you can use for the
further requests to **quotes** endpoints.
**b.** send a post request to `/api/v1/create_user` with JSON in the body of the request with your email
, your email and your desired password like this :

`{
    "username": "foo",
    "password": "foo+secretpass",
    "email": "foo@bar.com"
}`

if everything goes fine, then it returns a JSON with your email, username, id. after that
with your username and password, you can send a request to `/api/v1/get-token`, e.g. :

`{
    "username": "foo",
    "password": "foo+secretpass"
}`
Then it returns a JSON which includes a token so that you can use it in requests to **quotes** endpoints.

2- Right now, With the token or the API key, you can send a request to **quotes** APIs:
for all requests to **quotes** endpoints, you have to add **Authorization** header to your requests,
if you have an API key, the authorization header would be like this:
`{"Authorization": "Api-Key jIGOlx1g.WJ6xiO76oo4gAGVfNQpzg8tSh8SXDDLt"}`
but if you have Token, the header would be like :
`{"Authorization": "Token jIGOlx1g.WJ6xiO76oo4gAGVfNQpzg8tSh8SXDDLt"}`

- /api/v1/quotes 
By sending a **GET** request to this endpoint, you will receive a JSON containing **all** exchange rates.
With sending a **POST** request to this endpoint, you will force the app to fetch an alphavantage exchange rate and 
saves data into DB also, it returns 
that rate.
- /api/v1/latest_quote
If you send a get request to this endpoint, it returns the latest exchange rate from the DB.

