DROP DATABASE IF EXISTS barberDB;
CREATE DATABASE IF NOT EXISTS barberDB;

USE barberDB;

CREATE TABLE barbers (
    bname char(64),
    bphonum int,
    pass char(8)
);

CREATE TABLE customers (
    cname char(64),
    cphonum int,
    cdate date,
    ctime time
);

INSERT INTO barbers (bname, bphonum, pass)
VALUES ("John", 6901234567, "lemon"),
("Josh", 6912345678, "orange"),
("Son", 6901234567, "tomato");