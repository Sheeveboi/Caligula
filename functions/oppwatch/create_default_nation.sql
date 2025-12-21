-- DROP FUNCTION public.create_default_nation(text);

CREATE OR REPLACE FUNCTION public.create_default_nation(nation text)
 RETURNS TABLE(response_code integer, message text)
 LANGUAGE plpgsql
AS $function$

	DECLARE response record;

	BEGIN

		-- create new record
		INSERT INTO nations (nation_name, threat) VALUES (nation, 0);

		-- create 200 ok response
		FOR response IN (

			SELECT 

			200 as feather, 
			'Created Nation.' as alto

		) 
		LOOP

			response_code := response.feather;
			message       := response.alto;

			RETURN NEXT;

		END LOOP;
		
	END;
$function$
;
