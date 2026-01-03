-- DROP FUNCTION public.create_channel(int4, text, int4);

CREATE OR REPLACE FUNCTION public.create_channel(id integer, relay text, ctype integer)
 RETURNS TABLE(response_code integer, message text)
 LANGUAGE plpgsql
AS $function$

	DECLARE response record;

	BEGIN

		-- error handling
		-- if more than one channel connections share a relay group
		IF 
			id IN (

				SELECT channel_id FROM channels WHERE relay_group = relay 

			)

		-- send conflict error response
		THEN 

			FOR response IN (

				SELECT 

				400 as feather, 
				'Relay conflict! A channel may not connect to a relay group more than once.' as alto

			) 
			LOOP

				response_code := response.feather;
				message       := response.alto;

				RETURN NEXT;

			END LOOP;
	
		ELSE

			-- create new record
			INSERT INTO channels (channel_id, relay_group, channel_type) VALUES (id, relay, ctype);
	
			-- create new relay group if needed
			INSERT INTO relay_groups (relay_group, auto_alerts)
			SELECT relay, false
			WHERE relay NOT IN (SELECT relay_group from relay_groups);
	
			FOR response IN (
	
				SELECT 
	
				200 as feather, 
				'Created Channel.' as alto
	
			) 
			LOOP
	
				response_code := response.feather;
				message       := response.alto;
	
				RETURN NEXT;
	
			END LOOP;

		END IF;
		
	END;
$function$
;
