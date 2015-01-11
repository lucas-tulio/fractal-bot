-- Use this table to prevent sending fractals to the same person too often
create table logs (
  id int primary key auto_increment,
  username varchar(255) not null,
  created_at timestamp default current_timestamp
);
