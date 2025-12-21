

-- DROP FUNCTION public.remove_nation(text);

CREATE OR REPLACE FUNCTION public.remove_nation(nation text)
 RETURNS TABLE(response_code integer, message text)
 LANGUAGE plpgsql
AS $function$

	DECLARE response record;

	BEGIN
		
		IF nation NOT IN ( SELECT nation_name FROM nations ) THEN 

			FOR response IN ( 

				SELECT 

				404 as feather, 
				'Not Found! Nation not found with given nation_name.' as alto

			) 

			LOOP

				response_code := response.feather;
				message       := response.alto;

				RETURN NEXT;

			END LOOP;
		
		ELSE
		
			-- remove record
			DELETE FROM nations WHERE nation_name = nation;
			
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
;
