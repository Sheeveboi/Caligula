-- DROP FUNCTION public.create_snitch_hit(text, text, text, text, text, int4, int4, int4);

CREATE OR REPLACE FUNCTION public.create_snitch_hit(ign text, relay text, sname text, nl text, nation text, x integer, y integer, z integer)
 RETURNS TABLE(response_code integer, message text)
 LANGUAGE plpgsql
AS $function$

	DECLARE 
		response record;
	BEGIN

		-- create new record
		INSERT INTO 
			snitches (player, relay_group, snitch_name, name_layer, nation_name, x_cords, y_cords, z_cords) 
			VALUES (ign, relay, sname, nl, nation, x, y, z);


		-- create new player if does not exist
		IF ign NOT IN (SELECT username FROM players) THEN
			
			PERFORM create_default_player(ign);

		ELSE 

			UPDATE players
			SET 
				last_x = x,
				last_y = y,
				last_z = z
			WHERE 
				username = ign;

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
