-- DROP FUNCTION public.addreps();

CREATE OR REPLACE FUNCTION public.addreps(ign text, ammount int)
	RETURNS TABLE(response_code integer, message text)
	LANGUAGE plpgsql
AS $function$

	DECLARE response record;

	BEGIN

		IF ign NOT IN (SELECT username FROM players)

		THEN
			
			FOR response IN (

				SELECT 

				404 as feather, 
				'Not found!. Player not found with given ign.' as alto

			) 
			LOOP

				response_code := response.feather;
				message       := response.alto;

				RETURN NEXT;

			END LOOP;			

		END IF;

		UPDATE players

		SET reps = reps + ammount

		WHERE username = ign;

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

	END;
$function$
;
;
