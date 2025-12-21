-- DROP FUNCTION public.remove_player();

-- DROP FUNCTION public.remove_player(text);

CREATE OR REPLACE FUNCTION public.remove_player(ign text)
 RETURNS TABLE(response_code integer, message text)
 LANGUAGE plpgsql
AS $function$

	DECLARE response record;

	BEGIN
		
		IF ign NOT IN ( SELECT username FROM players ) THEN 

			FOR response IN ( 

				SELECT 

				404 as feather, 
				'Not Found! Player not found with given ign.' as alto

			) 

			LOOP

				response_code := response.feather;
				message       := response.alto;

				RETURN NEXT;

			END LOOP;
		
		ELSE
		
			-- remove record
			DELETE FROM players WHERE username = ign;
			
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
$function$;
