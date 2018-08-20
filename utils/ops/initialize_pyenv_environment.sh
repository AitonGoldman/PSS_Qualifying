curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
export PATH="~/.pyenv/bin:$PATH"
eval "$(~/.pyenv/bin/pyenv init -)"
eval "$(~/.pyenv/bin/pyenv virtualenv-init -)"
CFLAGS=-I/usr/include/openssl LDFLAGS=-L/usr/lib pyenv install -v 3.5.3
pyenv virtualenv 3.5.3 pss_venv
echo 'add the following to your .bashrc or .bash_profile'
echo 'eval $(~/.pyenv/bin/pyenv init -)'
echo 'eval $(~/.pyenv/bin/pyenv virtualenv-init -)'
echo ' '
echo 'use the following command to switch to the approriate version of python '
echo 'pyenv activate pss_venv'
