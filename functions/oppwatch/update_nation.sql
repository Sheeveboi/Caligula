-- DROP FUNCTION public.update_nation(text, text, int4, text, text);

CREATE OR REPLACE FUNCTION public.update_nation(nation text, new_name text, new_threat integer, new_img text, new_notes text)
 RETURNS TABLE(response_code integer, message text)
 LANGUAGE plpgsql
AS $function$

	DECLARE response record;

	BEGIN

		-- error handling
		-- if more than one channel connections share a relay group
		IF 
			nation NOT IN (

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
	
		ELSE

			-- remove old record
			DELETE FROM nations WHERE nation_name = nation;	

			-- create new record
			INSERT INTO nations (nation_name, threat, img_url, notes) VALUES (new_name, new_threat, new_img, new_notes);
	
			-- send 200 ok response
			FOR response IN (
	
				SELECT 
	
				200 as feather, 
				'Updated Nation.' as alto
	
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
