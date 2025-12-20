drop table channels; 	
create table channels(

	channel_id int not null, 
		-- this is technically a primary key, despite it not being written as such.
		-- However, as a trade off for simplicity, this behavior is enforced in a function instead.
		-- oppwatch_control functions are not called often, so the unomptimal nature of this approach is diminished. 
	
	relay_group text not null,
	channel_type int not null,

	notif_id int,
	
	check (channel_type <= 2)
);

drop table pos_igns;
create table pos_igns (
 	username text not null,
 	
 	primary key (username)
);
 	
drop table relay_groups;
create table relay_groups(
 	relay_group text not null,
 	
 	auto_alerts boolean, 
 	threshold int,
 	nation text, 
 	description text,
 	
 	check (threshold <= 3),
 	check (len(nation) <= 50),
 	check (len(description) < 250),
 	
 	primary key (relay_group)
);