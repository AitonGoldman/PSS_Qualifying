set -e
add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) main universe"
source ./utils/ops/list_of_packages_to_install.sh
apt-get update
for i in ${LIST_OF_PACKAGES[@]}
do
    apt-get --allow-downgrades --force-yes install $i    
done

sudo -u postgres psql template1 -c "create user tom"
sudo -u postgres psql template1 -c "alter user tom with password 'tom_password'"
sudo -u postgres psql template1 -c "alter user tom with SUPERUSER"

