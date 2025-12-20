-- DROP FUNCTION public.remove_channel(int4, text);

CREATE OR REPLACE FUNCTION public.remove_channel(id integer, relay text)
 RETURNS TABLE(response_code integer, message text)
 LANGUAGE plpgsql
AS $function$

	DECLARE response record;

	BEGIN
		
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

		ELSEIF relay NOT IN ( SELECT relay FROM channels WHERE channel_id = id) THEN 

			FOR response IN ( 

				SELECT 

				404 as feather, 
				'Not Found! Channel not connected to given relay group.' as alto

			) 

			LOOP

				response_code := response.feather;
				message       := response.alto;

				RETURN NEXT;

			END LOOP;
		
		ELSE
		
			DELETE FROM channels WHERE channel_id = id AND relay_group = relay;

			PERFORM check_and_delete_unused(relay);
			
			-- send response
			FOR response IN ( 

				SELECT 

				200 as feather, 
				'Channel Removed.' as alto

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
