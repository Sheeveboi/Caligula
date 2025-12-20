DROP FUNCTION public.create_channel(id integer, relay text, ctype int);

CREATE OR REPLACE FUNCTION public.create_channel(id integer, relay text, ctype int)
 RETURNS table (response_code int, message text)
 LANGUAGE plpgsql
AS $function$

	DECLARE response record;

	BEGIN

		-- error handling
		-- if more than one channel connections share a relay group
		IF 
			id NOT IN (
				SELECT channel_id FROM channels WHERE relay_group = relay 
			)

		-- send error response
		THEN 

			FOR response IN (
			SELECT 
				304 as return_response_code, 
				'A channel may not connect to a relay group more than once' as return__message
			) 
			LOOP
				response_code := return_response_code;
				message       := return_message;
			END LOOP;
			
		ELSE 

			INSERT INTO output_channels (channel_id, relay_group, channel_type) VALUES (id, relay, ctype);

			INSERT INTO relay_groups (relay_group)
			SELECT relay
			WHERE relay NOT IN (SELECT relay_group from relay_groups);
		
		END IF;
	END;
$function$;