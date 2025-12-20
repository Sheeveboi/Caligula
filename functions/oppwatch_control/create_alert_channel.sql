-- DROP FUNCTION public.create_alert_channel(int4, text);

CREATE OR REPLACE FUNCTION public.create_alert_channel(id integer, relay text)
 RETURNS bool
 LANGUAGE plpgsql
AS $function$
	BEGIN

		IF id NOT IN (
			SELECT channel_id FROM alert_channels WHERE relay_group = relay
		)
	
		THEN	 
		 
			INSERT INTO alert_channels (channel_id, relay_group) VALUES (id, relay);

			INSERT INTO relay_groups (relay_group)
			SELECT relay
			WHERE relay NOT IN (SELECT relay_group from relay_groups);

			RETURN TRUE;
			
		ELSE RETURN FALSE;
		
		END IF;
	END;
$function$
;

SELECT create_alert_channel(%s, %s);
