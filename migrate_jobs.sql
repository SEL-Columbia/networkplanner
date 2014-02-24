create table jobs_copy (
  pid integer not null, 
  host varchar(64) not null, 
  start_time datetime not null, 
  end_time datetime, 
  primary key (pid, host, start_time) 
);

insert into jobs_copy select * from jobs;

drop table jobs;

alter table jobs_copy rename to jobs;
