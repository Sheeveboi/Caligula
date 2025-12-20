drop table input_channels;
create table input_channels(
 	channel_id int not null,
 	relay_group text not null,
 	
 	notif_id int,
 	
 	primary key (channel_id)
 );
 drop table output_channels;
 create table output_channels(
 	channel_id int not null, -- channel_id does not need to be a primary key here, as we would theoretically want to condense multiple outputs into a single channel.
 	relay_group text not null,
 	
 	notif_id int
 );
 drop table alert_channels;
 create table alert_channels(
 	channel_id int not null, -- same here
 	relay_group text not null,
 	
 	notif_id int
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
 	
 	primary key (relay_group)
 );