drop table players;
create table players(

	username text not null,
	threat int not null,
	
	img_url text,
	notes text,
	nation text,
	last_snitch uuid, 
	reps int,
	
	last_x int,
	last_y int,
	last_z int,
	 
	check (LENGTH(notes) <= 2000),
	check (threat <= 3),
	check (
		(
			patindex('%http://', img_url) != 1 OR 
			patindex('%https://', img_url) != 1
		) 
		AND (LENGTH(img_url) <= 150)
	),
	
	primary key (username)
	
);

drop table nations;
create table nations(

	nation_name text not null,
	threat int not null,
	
	img_url text,
	notes text,
	 
	check (LENGTH(notes) <= 2000),
	check (threat <= 3),
	check (
		(
			patindex('%http://', img_url) != 1 OR 
			patindex('%https://', img_url) != 1
		) 
		AND (LENGTH(img_url) <= 150)
	),	
	
	primary key (nation_name)
	
);
drop table snitches;
create table snitches(
	
	player text not null,
	relay_group text not null,
	
	x_cords int not null,
	z_cords int not null,
	
	snitch_name text,
	name_layer text,
	nation text,
	y_cords int,
	
	hit_id uuid not null,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP,
	
	check (LENGTH(snitch_name) <= 75),
	check (LENGTH(name_layer) <= 75)
);