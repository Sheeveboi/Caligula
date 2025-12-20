INSERT INTO input_channels (channel_id, relay_group) 
VALUES (%s, %s);

INSERT INTO relay_group(name)
SELECT %s 
WHERE %s NOT IN (SELECT name from relay_group);