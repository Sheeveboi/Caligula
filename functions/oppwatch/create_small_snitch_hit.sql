-- DROP FUNCTION public.create_small_snitch_hit(text);

CREATE OR REPLACE FUNCTION public.create_small_snitch_hit(ign text, x float, y float, z float)
 RETURNS TABLE(response_code integer, message text)
 LANGUAGE plpgsql
AS $function$

	DECLARE 
		response record;
		new_uuid uuid;

	BEGIN

		new_uuid = get_random_uuid();

		-- create new record
		INSERT INTO snitches (player, x_cords, y_cords, z_cords) VALUES (ign, x, y, z);

		-- create new player if does not exist
		IF ign NOT IN (SELECT username FROM players) THEN
			
			PERFORM create_default_player(ign);

		END IF;

		-- create 200 ok response
		FOR response IN (

			SELECT 

			200 as feather, 
			CONCAT('Created snitch hit. Hit ID is ', new_uuid) as alto

		) 
		LOOP

			response_code := response.feather;
			message       := response.alto;

			RETURN NEXT;

		END LOOP;
		
	END;
$function$
;
