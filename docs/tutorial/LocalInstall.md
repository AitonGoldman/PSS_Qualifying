# On Ubuntu
- Clone the PSS_Qualifying repo
  - `git clone https://github.com/AitonGoldman/PSS_Qualifying.git`
- Run the package install script to install all needed packages 
  - `cd PSS_Qualifying; bash utils/ops/install_packages.sh`
- Run the pyenv initialization script to install pyenv and python 3 
  - `source utils/ops/initialize_pyenv_environment.sh`
  - `pyenv` allows you to easily manage (and switch between) multiple versions of python
  - After running the pyenv initialization script, it will ask you to add 2 lines to your bashrc or bash_profile.  Do it
  - Start a new shell to pickup the changes
  
# On OS X
- Clone the PSS_Qualifying repo
  - `git clone https://github.com/AitonGoldman/PSS_Qualifying.git`
- Install homebrew :
  - Instructions on how to install homebrew at https://brew.sh/
- Run the package install script to install all needed packages 
  - `cd PSS_Qualifying; bash utils/ops/install_packages_on_osx.sh`
- Run the pyenv initialization script to install pyenv and python 3 
  - `source utils/ops/initialize_pyenv_environment_on_osx.sh`
  - `pyenv` allows you to easily manage (and switch between) multiple versions of python
  - After running the pyenv initialization script, it will ask you to add 2 lines to your bashrc or bash_profile.  Do it
  - Start a new shell to pickup the changes
  

# On Both
- Create a directory `ignore` under the top level PSS_Qualifying directory and a file in that directory - add the following to the file - you must source the file before you run the PSS_Qualifying server
 ```
   export pss_db_name=test
   export db_username=tom
   export db_password=tom_password
   export FLASK_SECRET_KEY=fake_key
 ```

- Activate the python environment 
  - `pyenv activate pss_venv`
- Run the database bootstrapping script to create the database (name 'test')
  - `PYTHONPATH=. python utils/populate/create_db.py test`  
- create alias for `gunicorn` to pyenv dir - `gunicorn` is needed for running the PSS server
  - `alias gunicorn=``pyenv prefix``/bin/gunicorn`
  - add the alias command to your .bashrc

