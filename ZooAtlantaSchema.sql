-- # Animal House CS 4400 | Relational Schema
-- # last modified: 11/5/2018

-- InnoDB configuration
-- innodb_file_per_table=1
-- innodb_file_format=barracuda
-- innodb_strict_mode=1
create database if not exists cs4400_group4;
use cs4400_group4;

create table USERS (
    email varchar(32),
    username varchar(32),
    password varchar(32) not null,
    user_type varchar(10) not null,
    primary key (email, username)
) Engine = Innodb;


create table EXHIBITS (
    exhibit_name varchar(32) primary key,
    water text not null,
    number_of_animals int not null,
    size int not null
) Engine = Innodb;


create table SHOWS (
    show_name varchar(32),
    datetime DATETIME not null,
    exhibit_name varchar(32) references EXHIBITS(exhibit_name)
        on delete cascade
        on update cascade,
    username varchar(32) references USERS(username),
    primary key (show_name, datetime)
) Engine = Innodb;


create table ANIMALS (
    name varchar(32),
    species varchar(32),
    type varchar(32) not null,
    age int not null,
    exhibit_name varchar(32) references EXHIBITS(exhibit_name)
        on delete cascade
        on update cascade,
    primary key (name, species)
) Engine = Innodb;


create table ANIMAL_CARE (
    name varchar(32) references ANIMALS(name)
        on delete cascade
        on update cascade,
    species varchar(32) references ANIMALS(species)
        on delete cascade
        on update cascade,
    username varchar(32) references USERS(username)
        on delete cascade
        on update cascade,
    datetime DATETIME not null,
    note varchar(255),
    primary key (username, datetime)
) Engine = Innodb;


create table SHOW_VISITS (
    show_name varchar(32) references SHOWS(show_name)
        on delete cascade
        on update cascade,
    datetime DATETIME not null,
    username varchar(32) references USERS(username)
        on delete cascade
        on update cascade,
    primary key (username, show_name, datetime)
) Engine = Innodb;


create table EXHIBIT_VISITS (
    exhibit_name varchar(32) references EXHIBITS(exhibit_name)
        on delete cascade
        on update cascade,
    username varchar(32) references USERS(username)
        on delete cascade
        on update cascade,
    datetime DATETIME not null,
    primary key (exhibit_name, username, datetime)
) Engine = Innodb;
