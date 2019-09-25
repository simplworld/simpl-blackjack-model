# simpl-calc-model - example single-player simulation model service.

## Python Setup (assumes Python >= 3.6 and simpl-games-api server running)

```shell
$ git clone git@github.com:simplworld/simpl-calc-model.git
$ cd simpl-calc-model
$ mkvirtualenv simpl-calc-model
$ add2virtualenv .

$ pip install -r requirements.txt
```
## Run model service

```shell
$ export DJANGO_SETTINGS_MODULE=simpl_calc_model.settings
$ ./manage.py run_modelservice
```

If you need some serious debugging help, the model_service includes the ability to do

```shell
$ ./manage.py run_modelservice --loglevel=debug
```

Which will turn on verbose debugging of the Autobahn/Crossbar daemon to help debug interactions between the browser and model service backend.

## Run unit tests

```shell
$ pytest
```

## Development commands:

### 1 - To setup up database for simpl-calc development use:

1. Creates the simpl-calc game with one phase (Play) and one role (Calculator).
1. Adds a 'default' run..
1. Adds 1 leader ('leader@calc.edu'/'leader') to the run.
1. Adds 2 players to the run ('s#@calc.edu'/'s#' where # is between 1..2. Each player has a private scenario and period 1.
1. The run is set to 'Play' phase

execute:

```shell
$ ./manage.py create_default_env
```

To make it easier to recreate the default run you can pass the `--reset` option to delete the
default run and recreate it from scratch like this:

```shell
$ ./manage.py create_default_env --reset
```

### 2 - To submit a decision on a scenario:

```shell
$ ./manage.py submit_decision -s <scenario_id> -d <decision>
```

Copyright © 2018 The Wharton School,  The University of Pennsylvania 

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

