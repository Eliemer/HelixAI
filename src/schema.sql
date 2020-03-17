/*
This script provides the schema for the database.
This file is exclusively SQL queries
*/
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Experiment;
DROP TABLE IF EXISTS Team;
DROP TABLE IF EXISTS Config;
DROP TABLE IF EXISTS User_in_Team;

CREATE TABLE User (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  premium BOOLEAN NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE Team (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  premium BOOLEAN NOT NULL,
  name TEXT UNIQUE NOT NULL,
  description TEXT
);

CREATE TABLE Config (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  model TEXT NOT NULL,
  dataset TEXT NOT NULL,
  metrics TEXT NOT NULL
);

CREATE TABLE Experiment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  team_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  name TEXT NOT NULL,
  description TEXT,
  config_id INTEGER NOT NULL,

  FOREIGN KEY (team_id) REFERENCES Team (id),
  FOREIGN KEY (config_id) REFERENCES Config (id)
);

CREATE TABLE User_in_Team (
  usr_id INTEGER NOT NULL,
  team_id INTEGER NOT NULL,

  PRIMARY KEY (usr_id, team_id)
);
