# DSC Website Backend
Welcome to the backend for official [DSC HIT](https://dschit.com) website.

This is a **Python 3** and **Flask** based REST API which uses [Firebase](https://firebase.google.com/) for datastore.

## Documentation
There are 2 steps to deploy.
1. [Setup Firebase](#setup-firebase)
2. [Deploy on Heroku](#deploy-on-heroku)

### Setup Firebase
1. Create a Firebase project & generate keys for a [Firebase Service Account](https://firebase.google.com/docs/admin/setup#set-up-project-and-service-account).
2. Save the credential file as `key.json` in your project root. <br>**IMPORTANT** *Don't forget to add* `key.json` *to your* `.gitignore` *file so you don't accidentally commit it*.
3. Export the `key.json` contents through an environment variable depending on your development platform. For **Linux** I use [direnv](https://github.com/direnv/direnv) with a `.envrc` file which looks something like the following
```bash
...
export FIREBASE_CERT=$(cat key.json)
...
```

### Deploy on Heroku
1. Setup [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true#set-up) on local machine.
2. Setup Heroku [config variables](https://devcenter.heroku.com/articles/config-vars). These variables can be accessed using the Pyhton `os.environ` variable. For this project, create a config variable named `FIREBASE_CERT` and paste the contents of the `key.json` file as value.
3. If you have used Heroku dashboard to create the app then you need to setup git remote for [Heroku](https://devcenter.heroku.com/articles/git#creating-a-heroku-remote).
4. Finally, push the code to *heroku* remote and it will be deployed automatically.

### Testing Locally
1. Create a virtual environment in project root
```bash
python3 -m venv venv
```
2. Activate the `venv`
```bash
source ./venv/bin/activate
```
3. Install the dependencies using `pip`
```bash
pip install -r requirements.txt
```
4. **[OPTIONAL]** Export the environment variable `FLASK_ENV`
```bash
# this line may also be added in .envrc file
export FLASK_ENV=development
```
5. Run flask app
```bash
flask run
```