"""Set up your virtual environment for development"""
import os, subprocess

subprocess.call([
   'pip3',
   'install',
   '-r',
   'requirements.txt'
])
subprocess.call([
   'pip3',
   'install',
   '-e',
   'git+http://github.com/russ-/pychallonge#egg=pychallonge'
])
