# Creating a VM with virtualbox

When running commands using sudo, it will ask you for a password.  Give the password for the account you are logged in as.

- Get the latest version of VirtualBox
- Get the latest version of the ubuntu server iso ( https://www.ubuntu.com/download/server )
- Create a new VM for a 64 bit linux (accepting all the defaults)
- Once the VM is created, point "insert" the ubuntu iso into the virtual cd rom 
  - See this link for details on how to do this : https://askubuntu.com/questions/64915/how-do-i-install-ubuntu-on-a-virtualbox-client-from-an-iso-image
- Start the VM and go through the ubuntu install process
- "Remove" the iso from the virtual cd rom and let the VM restart
  - When you have the VM window selected, under the "Devices" menu, select "Optical Drives" -> "Remove Disc..."
- Once the VM has restarted, login to VM
- While the VM window is selected, under the "Devices" menu, select "Insert guest additions..."
- In the VM, run the following command to install needed packages : `sudo apt-get install gcc make build-essential`
- In the VM, run the following command to mount the cdrom and install the virtualbox guest additions : `mkdir /media/cdrom;mount /dev/cdrom /media/cdrom` and then 'cd /media/cdrom;sudo sh VboxLinuxAdditions.run'
- sudo adduser $USER vboxsf
  - $USER is set to the user you created as part of the ubuntu installation process
- Reboot the VM
- Add a shared folder to the VM - this will let you edit/view files in your host OS
  -  Follow the instructions here : https://www.youtube.com/watch?v=89HDKvTfR_w
- Reboot the VM 
- Login to the VM and look in `/media` as root 
  - You will see a directory that has the same name as the shared folder you created - this directory is shared between your guest and host OS
- Goto the shared folder directory under '/media' and clone the PSS_Qualifying repo
  - `git clone https://github.com/AitonGoldman/PSS_Qualifying.git`
- Run the package install script to install all needed packages 
  - `cd PSS_Qualifying; bash utils/ops/install_packages_for_vm.sh`
- Add the following to your .bashrc in the VM  and source your .bashrc
 ```
   export pss_db_name=test
   export db_username=tom
   export db_password=tom_password
   export FLASK_SECRET_KEY=fake_key
 ```
- run setup.py in top level directory of PSS_Qualifying - this will install all the needed Python packages
  - `python setup.pyenv.py` 
- run populate script
  - `PYTHONPATH=. python utils/populate/create_db.py test`
- add forwarded port to virtual box - this will let you reach the server from your host OS
  - ???
