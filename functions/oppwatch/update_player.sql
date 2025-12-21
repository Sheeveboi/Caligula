-- DROP FUNCTION public.update_player();

CREATE OR REPLACE FUNCTION public.update_player(ign text, new_ign text, new_threat int, new_img text, new_notes text, new_nation text)
 RETURNS TABLE(response_code integer, message text)
 LANGUAGE plpgsql
AS $function$

	DECLARE response record;

	BEGIN

		-- error handling
		-- if more than one channel connections share a relay group
		IF 
			new_nation NOT IN (

				SELECT nation_name FROM nations

			)

		-- send conflict error response
		THEN 

			FOR response IN (

				SELECT 

				404 as feather, 
				'Not found!. Nation not found with given nation_name.' as alto

			) 
			LOOP

				response_code := response.feather;
				message       := response.alto;

				RETURN NEXT;

			END LOOP;

		ELSEIF 
	
			ign NOT IN (

				SELECT username FROM players

			)

		-- send conflict error response
		THEN 

			FOR response IN (

				SELECT 

				404 as feather, 
				'Player not found.' as alto

			) 
			LOOP

				response_code := response.feather;
				message       := response.alto;

				RETURN NEXT;

			END LOOP;
	
		ELSE

			-- remove old record
			DELETE FROM players WHERE username = ign;	

			-- create new record
			INSERT INTO players (username, threat, img_url, notes, nation) VALUES (new_ign, new_threat, new_notes, new_nation);
	
			-- send 200 ok response
			FOR response IN (
	
				SELECT 
	
				200 as feather, 
				'Updated Player.' as alto
	
			) 
			LOOP
	
				response_code := response.feather;
				message       := response.alto;
	
				RETURN NEXT;
	
			END LOOP;

		END IF;
		
	END;
$function$;

