-- DROP FUNCTION public.update_channel(int4, text, int4, text, int4);

CREATE OR REPLACE FUNCTION public.update_channel(id integer, relay text, new_relay text, new_channel_type integer, new_notif_id integer)
 RETURNS TABLE(response_code integer, message text)
 LANGUAGE plpgsql
AS $function$

	DECLARE response record;

	BEGIN
				
		-- error handling

		-- throw 404 if channel cant be found by ID 
		IF id NOT IN ( SELECT channel_id FROM channels ) THEN 

			FOR response IN ( 

				SELECT 

				404 as feather, 
				'Not Found! Channel connection not found with given id.' as alto

			) 

			LOOP

				response_code := response.feather;
				message       := response.alto;

				RETURN NEXT;

			END LOOP;

		-- if more than one channel connections share a relay group
		ELSEIF id IN ( SELECT channel_id FROM channels WHERE relay_group = new_relay ) THEN 

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

		-- update channel
		ELSE 	

			-- remove old record
			DELETE FROM channels WHERE channel_id = id AND relay_group = relay;		

			-- create new record
			INSERT INTO channels (channel_id, relay_group, channel_type) VALUES (id, relay, new_channel_type);

			-- clean up relay group if unused
			PERFORM check_and_delete_unused(relay);

			-- create new relay group record if the new relay doesnt exist
			INSERT INTO relay_groups (relay_group)
			SELECT new_relay
			WHERE new_relay NOT IN (SELECT relay_group FROM relay_groups);

			FOR response IN (

				SELECT 

				200 as feather, 
				'Updated channel' as alto

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
