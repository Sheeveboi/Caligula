-- DROP FUNCTION public.create_output_channel();

CREATE OR REPLACE FUNCTION public.create_output_channel(id integer, relay text)
 RETURNS bool
 LANGUAGE plpgsql
AS $function$
	BEGIN

		IF id NOT IN (
			SELECT channel_id FROM output_channels WHERE relay_group = relay
		)
	
		THEN	 
		 
			INSERT INTO output_channels (channel_id, relay_group) VALUES (id, relay);

			INSERT INTO relay_groups (relay_group)
			SELECT relay
			WHERE relay NOT IN (SELECT relay_group from relay_groups);

			RETURN TRUE;
			
		ELSE RETURN FALSE;
		
		END IF;
	END;
$function$
;

SELECT create_output_channel(%s, %s);