-- DROP FUNCTION public.create_input_channel();

CREATE OR REPLACE FUNCTION public.create_input_channel(id integer, relay text)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
	BEGIN
		INSERT INTO input_channels (channel_id, relay_group) 
		VALUES (id, relay);
		
		INSERT INTO relay_groups (relay_group)
		SELECT relay 
		WHERE relay NOT IN (SELECT relay_group from relay_groups)

		AND 0 in (

			SELECT COUNT(*) from input_channels

			WHERE channel_id  = id
			AND   relay_group = relay

		);

		RETURN 0;
	END;
$function$
;

SELECT create_input_channel(%s, %s);