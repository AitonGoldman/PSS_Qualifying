# PSS Qualifying Architecture

## Overview
The PSS_Qualifying component is a server that handles all the functionality needed during the qualifying phase of a tournament.  It exposes a REST api and saves it's information in a postgres database.  It uses the Flask framework (http://flask.pocoo.org/docs/1.0/) to create the REST api, and SQLalchemy (http://docs.sqlalchemy.org/en/latest/orm/tutorial.html) to communicate with the database. 

## The 3 parts of PSS Qualifying
PSS Qualifying is split into 3 parts :

- The business logic : This is the code that implements the logic behind the features (i.e. recording a score, adding someone to a queue, purchasing a ticket ) as Flask routes 
- The database : The tables in the database
- The database access code : The code that uses SQLalchemy to query the database and insert data into the database.  This code will be used by the business logic code to access the database. 

The expectation is that these different layers will be kept as separate as possible.  This means that the business logic layer will have no knowledge of the database access code internals.  Business logic code will not directly call SQLAlchemy code and business logic code will not be expected to handle SQLalchemy exceptions.  The flip side of this is that database access code will have no knowledge of the business logic code.  It will not throw Flask exceptions and it will not access any of Flask's builtin functionality (i.e. getting HTTP request data directly) 

Users will not directly interact with the PSS_Qualifying server, but instead will interact with a separate frontend component.  This frontend component will be responsible for calling the PSS_Qualifying REST api.

## Features

PSS_Qualifying will implement the following features : 
- management of events
- management of competitions in events
- management of competition officials (i.e. tournament directors, scorekeepers, etc) for each event
- ticket purchases
- register players for events
- allow players to be queued (and removed from queues) for each machine in the competition
- allow players to add themselves/remove themselves from queues
- allow players to directly purchase tickets
- record/void scores 
- report ranked results to players
- use Firebase to notify players when their queue positions have changed
- send emails to players (when needed)

## A brief explanation of the entities in the database and their relationship

Players play in a `Event` which is made up of one or more `Competitions`.  For example, Papa 20 would be an `Event` and Classics II would be a `Competition`. `Players` purchase `Tickets` which allow them to play one or more `Games`.  `Scores` on the `Games` are recorded and then ranked per `Game` and rankings in a `Competition` are calculated based on the per `Game` rankings. `Players` can be placed on a `Queue` for each `Game`.  `Tournament Directors` and `Scorekeepers` are able to login to the system to run the `Event` (i.e. scorekeep, purchase people tickets, etc).  `Players` can also login to purchase `Tickets` directly or add/remove themselves from the `Queue`.

A more detailed look at the tables in the database are here
