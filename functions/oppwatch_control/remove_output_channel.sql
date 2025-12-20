DELETE FROM relay_groups as r

WHERE relay_group IN (

	SELECT relay_group AS name FROM input_channels
	WHERE channel_id = %s

	AND 1 IN (
		SELECT COUNT(relay_group) from input_channels as i	
		WHERE r.relay_group = i.relay_group
	)

	AND 0 IN (
		SELECT COUNT(relay_group) from output_channels as o
		WHERE r.relay_group = o.relay_group
	)

	and 0 IN (
		SELECT COUNT(relay_group) from alert_channels as a
		WHERE r.relay_group = a.relay_group
	)
);

DELETE FROM output_channels WHERE channel_id = %s;