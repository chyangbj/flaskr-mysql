drop table if exists entries;
create table entries (
  id integer primary key auto_increment,
  title text not null,
  text text not null,
  post_date datetime not null
);
create table users (
  id integer not null primary key auto_increment,
  name varchar(20) not null,
  password varchar(40) not null,
  email varchar(100) not null,
  reg_date datetime not null,
  last_login_date datetime not null,
  index(name),
  unique(username),
  unique(email)
)engine=innodb
