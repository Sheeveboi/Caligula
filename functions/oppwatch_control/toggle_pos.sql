-- DROP FUNCTION public.toggle_pos(text);

CREATE OR REPLACE FUNCTION public.toggle_pos(ign text)
 RETURNS TABLE(response_code integer, message text)
 LANGUAGE plpgsql
AS $function$

declare 
 	pos bool;
	response record;
BEGIN
	IF ign NOT IN (SELECT username FROM pos_igns) THEN
		
		INSERT INTO pos_igns (username) VALUES (ign);

		pos := 'True';
		
	ELSE 
	
		DELETE FROM pos_igns WHERE username = ign;

		pos := 'False';
		
	END IF;

	FOR response IN (

		SELECT 

		200 as feather, 
		CONCAT('Toggled POS! ', ign, ' marked as POS:', pos) as alto

	) 
	LOOP

		response_code := response.feather;
		message       := response.alto;

		RETURN NEXT;

	END LOOP;

END;
$function$;
