# Installation


### Vagrant (optional)

You can run project in Vagrant.

First, install vagrant and VirtualBox:
```bash
# Ubuntu
sudo apt-get install vagrant virtualbox
```

To start Vagrant box use:
```bash
vagrant up
```

To log into Vagrant box type:
```bash
vagrant ssh
```

### Prerequisites

Install the following dependencies:
```bash
# Ubuntu
sudo apt-get install virtualenv gcc python3-dev gettext python3-pip postgresql postgresql-contrib
```

Create virtual environment:
```bash
virtualenv --python=python3 ~/.virtualenv
```

Install python dependencies:
```bash
source ~/.virtualenv/bin/activate
pip3 install -r requirements.txt
```


# Database setup

Switch to postgresql user:
```bash
sudo -i -u postgres
```

Create new postgres role, database and set password for role
```bash
createuser --interactive
createdb <database_name>
ALTER ROLE <role_name> SET PASSWORD '';
```


# Run

Start django debug session.
```bash
source ~/.virtualenv/bin/activate
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver 0.0.0.0:8000
```

If you would like to load sample data use:
```bash
./manage.py load_teams
```


## Webpack Installation

Install Node.js from https://nodejs.org/en/

In your project folder, create package.json file.
```bash
npm init -y
```
development only
```bash
npm install webpack --save-dev
npm install babel-preset-es2015 --save-dev
npm install node-sass --save-dev
npm install css-loader sass-loader scss-loader file-loader image-webpack-loader style-loader url-loader html-loader extract-text-webpack-plugin babel-core babel-loader clean-webpack-plugin html-webpack-plugin angular-cookies angular-route bootstrap jquery.countdown bootstrap-material-design --save-dev
```
Alternatively after pulling project with file package.json already created:

1. Install Node.js;
2. Install Webpack;

```bash
  npm install webpack@<<version from package.json file>> --save-dev
```

3. Install all dependencies from package.json file locally:

```bash
npm install
```

Webpack should compile files after every change, run:
```bash
npm run build:watch
```
Run before commit:
```bash
npm run build:prod
```

## Translations

Update message translation:
```bash
./manage.py makemessages -l pl
```

and compiled by:
```bash
./manage.py compilemessages
```