INSERT INTO output_channels (channel_id, relay_group) VALUES (%s, %s);

INSERT INTO relay_groups (relay_group)
SELECT %s 
WHERE %s NOT IN (SELECT relay_group from relay_groups);
