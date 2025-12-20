DELETE FROM relay_groups (relay_group)
SELECT relay_group AS FROM input_channels WHERE channel_id = %s; FROM input_channels WHERE channel_id = %s;

-- delete if this relay group exists
WHERE name IN (
	SELECT relay_group from relay_groups
)

-- delete if no channenls are using this relay group
-- the input channel check here looks for one, because the channel hasnt been deleted yet
WHERE 1 IN (
	SELECT COUNT(relay_group) from input_channels	
	WHERE relay_group = name
);

WHERE 0 IN (
	SELECT COUNT(relay_group) from output_channels	
	WHERE relay_group = name
);

WHERE 0 IN (
	SELECT COUNT(relay_group) from alert_channels	
	WHERE relay_group = name
);

DELETE FROM input_channels WHERE channel_id = %s;