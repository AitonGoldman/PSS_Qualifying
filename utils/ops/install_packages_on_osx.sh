set -e
source ./back/utils/ops/list_of_brews_to_install.sh
for i in ${LIST_OF_PACKAGES[@]}
do
    brew install $i    
done

psql template1 -c "create user tom"
psql template1 -c "alter user tom with password 'tom_password'"
psql template1 -c "alter user tom with SUPERUSER"
