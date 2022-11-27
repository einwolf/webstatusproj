# Web Status Project

A web project about computer status.

## Postgres Setup

```bash
psql -U postgres                # local
psql -U postgres -h 127.0.0.1   # ipv4
pg_ctl reload
```

```sql
/*
 * Setup a user for the project.
 * Users always have encrypted passwords starting with postgres 10.0.
 */
CREATE DATABASE webstatusproject;
CREATE USER webstatususer WITH PASSWORD 'webstatuspassword';
-- ALTER USER webstatususer WITH PASSWORD 'webstatuspassword';
ALTER ROLE webstatususer SET client_encoding TO 'utf8';
ALTER ROLE webstatususer SET default_transaction_isolation TO 'read committed';
ALTER ROLE webstatususer SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE webstatusproject TO webstatususer;
```

## Django setup

```bash
# Django setup commands
django-admin startproject webstatus
mkdir webstatus/frontend webstatus/templates webstatus/static

# edit settings.py

# Django dev
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

# Task and scheduling workers
python manage.py rundramatiq
python manage.py runapscheduler

# Setup after running migrate
python manage.py createsuperuser
```

## Nodejs setup commands

```bash
# Nodejs setup
mkdir webstatus/frontend
cd webstatus/frontend

npm install --save-dev @babel/cli @babel/core @babel/preset-env @babel/preset-react @babel/register babel-loader
npm install --save-dev webpack-cli webpack webpack-bundle-tracker
npm install react react-dom react-scripts
npm install @testing-library/jest-dom @testing-library/react @testing-library/user-event

# Run nodejs in watch mode to rebuild files during development
cd webstatus/frontend
npm run watch

# Static build all bundles once for production
cd webstatus/frontend
npm run build
```

## Redis commands

```bash
redis-cli ping
redis-cli -h host -p 6379 ping
redis-cli info

redis-cli --scan --pattern "*"
```
