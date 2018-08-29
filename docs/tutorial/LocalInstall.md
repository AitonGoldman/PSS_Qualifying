# On Ubuntu
- Clone the PSS_Qualifying repo
  - `git clone https://github.com/AitonGoldman/PSS_Qualifying.git`
- Run the package install script to install all needed packages 
  - `cd PSS_Qualifying; bash utils/ops/install_packages.sh`
  
# On OS X
- Clone the PSS_Qualifying repo
  - `git clone https://github.com/AitonGoldman/PSS_Qualifying.git`
- Install homebrew :
  - Instructions on how to install homebrew at https://brew.sh/
- Run the package install script to install all needed packages 
  - `cd PSS_Qualifying; bash utils/ops/install_packages_on_osx.sh`

# On Both
- run setup.py in top level directory of PSS_Qualifying - this will install all the needed Python packages
  - `python3 setup.pyenv.py` 

- Create a directory `ignore` under the top level PSS_Qualifying directory and a file in that directory - add the following to the file - you must source the file before you run the PSS_Qualifying server
 ```
   export pss_db_name=test
   export db_username=tom
   export db_password=tom_password
   export FLASK_SECRET_KEY=fake_key
 ```

- run populate script to populate database
  - `PYTHONPATH=. python3 utils/populate/create_db.py test`  
  

