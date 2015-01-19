create schema fractal;
use fractal;

-- Use this table to prevent sending fractals to the same person too often
create table logs (
  id int primary key auto_increment,
  username varchar(255) not null,
  created_at timestamp default current_timestamp
);

-- Do not send fractals to users in this table
create table blacklist (
  id int primary key auto_increment,
  username varchar(255) not null,
  created_at timestamp default current_timestamp
);

-- Log the fractal of the day
create table fotd (
  id int primary key auto_increment,
  link varchar(255) not null,
  deletehash varchar(255) not null,
  size int not null,
  created_at timestamp default current_timestamp
);
