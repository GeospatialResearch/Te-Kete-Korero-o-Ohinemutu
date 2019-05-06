# vue-webpack4-template
VueJs template using Webpack 4

This repository is an implementation of the 'Vue.js and Webpack 4 From Scratch' article series on [itnext.io](https://itnext.io).

[![Build Status](https://travis-ci.com/dfcook/vue-webpack4-template.svg?branch=master)](https://travis-ci.com/dfcook/vue-webpack4-template)

[Part 1](https://itnext.io/vuejs-and-webpack-4-from-scratch-part-1-94c9c28a534a):
  - Hot Module loading with webpack-dev-server
  - Linting using eslint
  - CSS pre-processing with stylus
  - Testing using @vue/test-utils and Jest

[Part 2](https://itnext.io/vue-js-and-webpack-4-from-scratch-part-2-5038cc9deffb):
  - Stylus for adding pre-processed CSS
  - Hot Module Reloading and HTML injection
  - Babel for building our scripts

[Part 3](https://itnext.io/vue-js-and-webpack-4-from-scratch-part-3-3f68d2a3c127):
  - Static assets processing
  - ESLint for linting
  - Testing using Jest
    - _For debugging the tests, first need to open `chrome:inspect` on Google Chrome and click the Open dedicated DevTools for Node then run the command `npm run test:debug` from your console._


### Django management
There's a few django commands available:

 * `make-migrations` will run the manage.py makemigrations command.
 * `make migrate` will run the migrate command, applying migrations.
 * `get-db` will get you an interactive shell for the database, so you can explore postgres
 * `initialise-db` will migrate, create an admin user (admin, admin@example.com, password) so you can log into django-admin and then loads test data.
 * `reset-db` will give you a clean slate database.
