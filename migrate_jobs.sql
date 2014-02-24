create table jobs_copy (
  pid integer not null, 
  host varchar(64) not null, 
  start_time timestamp without time zone not null, 
  end_time timestamp without time zone, 
  primary key (pid, host, start_time) 
);

insert into jobs_copy select * from jobs;

drop table jobs;

alter table jobs_copy rename to jobs;
