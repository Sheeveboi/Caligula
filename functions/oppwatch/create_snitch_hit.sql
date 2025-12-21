-- DROP FUNCTION public.create_snitch_hit(text, text, text, text, text);

CREATE OR REPLACE FUNCTION public.create_snitch_hit(ign text, relay text, sname text, nl text, nation text, x float, y float, z float)
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

		-- create 200 ok response
		FOR response IN (

			SELECT 

			200 as feather, 
			CONCAT('Created snitch hit.') as alto

		) 
		LOOP

			response_code := response.feather;
			message       := response.alto;

			RETURN NEXT;

		END LOOP;
		
	END;
$function$
;
