# PSS_Qualifying
PSS_Qualifying is a server that provides the functions needed to run the qualifying phase of a pinball tournament

# How to run PSS_Qualifying 

- Follow the instructions [docs/tutorial/LocalInstall.md](here) to install the pre-reqs.
- Run the server : `PYTHONPATH=. gunicorn -b 0.0.0.0:8000 'app:create_app' -w 1 --reload`

The server can now be reached on port 8000

# How to help

Read the [docs/tutorial/Tutorial.md](Quick Intro). 
