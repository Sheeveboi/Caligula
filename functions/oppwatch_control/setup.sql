 create table input_channels(
 	channel_id int not null,
 	relayGroup text not null,
 	
 	notif_id int,
 	
 	primary key (channel_id)
 );
 
 create table output_channels(
 	channel_id int not null, -- channel_id does not need to be a primary key here, as we would theoretically want to condense multiple outputs into a single channel.
 	relayGroup text not null,
 	
 	notif_id int
 );
 
 create table alert_channels(
 	channel_id int not null, -- same here
 	relayGroup text not null,
 	
 	notif_id int
 );
 
 create table pos_igns (
 	username text not null,
 	
 	primary key (username)
 );
 
 create table relay_groups(
 	name text not null,
 	
 	auto_alerts boolean, 
 	threshold int,
 	nation text, 
 	description text,
 	
 	primary key (name)
 );