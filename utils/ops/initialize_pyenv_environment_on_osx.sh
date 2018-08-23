eval "$(~/.pyenv/bin/pyenv init -)"
eval "$(~/.pyenv/bin/pyenv virtualenv-init -)"
CFLAGS="-I$(brew --prefix openssl)/include" LDFLAGS="-L$(brew --prefix openssl)/lib" pyenv install -v 3.5.3
pyenv virtualenv 3.5.3 pss_venv
echo 'add the following to your .bashrc or .bash_profile'
echo 'eval $(~/.pyenv/bin/pyenv init -)'
echo 'eval $(~/.pyenv/bin/pyenv virtualenv-init -)'
echo ' '
echo 'use the following command to switch to the approriate version of python '
echo 'pyenv activate pss_venv'
