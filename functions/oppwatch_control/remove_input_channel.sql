DELETE FROM input_channels WHERE channel_id = %s;

DELETE FROM relay_groups (relay_group)
SELECT %s 

-- delete if this relay group exists
WHERE %s IN (
	SELECT relay_group from relay_groups
)

-- delete if no channenls are using this relay group
WHERE 0 NOT IN (
	SELECT COUNT(relay_group) from input_channels	
	WHERE relay_group = %s
	
	UNION
	
	SELECT COUNT(relay_group) from output_channels	
	WHERE relay_group = %s
	
	UNION
	
	SELECT COUNT(relay_group) from alert_channels	
	WHERE relay_group = %s
);