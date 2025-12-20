-- DROP FUNCTION public.create_alert_channel();

CREATE OR REPLACE FUNCTION public.create_alert_channel(id int, relay text)
	RETURNS int4
	LANGUAGE plpgsql
AS $$
	BEGIN
		INSERT INTO alert_channels (channel_id, relay_group) VALUES (id, relay);

		INSERT INTO relay_groups (relay_group)
		SELECT id
		WHERE id NOT IN (SELECT relay_group from relay_groups);
	END;
$$;


SELECT create_alert_channel(%s, %s);