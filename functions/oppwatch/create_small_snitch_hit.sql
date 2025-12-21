-- DROP FUNCTION public.create_snitch_hit(text, text, text, text, text);

CREATE OR REPLACE FUNCTION public.create_snitch_hit(ign text, relay text, sname text, nl text, nation_name text)
 RETURNS TABLE(response_code integer, message text)
 LANGUAGE plpgsql
AS $function$

	DECLARE 
		response record;
		new_uuid uuid;

	BEGIN

		new_uuid = get_random_uuid();

		-- create new record
		INSERT INTO 
			snitches (player, relay_group, created_at, hit_id, snitch_name, name_layer, nation_name) 
			VALUES (ign, relay, CURRENT_TIMESTAMP, new_uuid, sname, nl, nation);

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
