-- DROP FUNCTION public.check_and_delete_unused(text);

CREATE OR REPLACE FUNCTION public.check_and_delete_unused(relay text)
 RETURNS boolean
 LANGUAGE plpgsql
AS $function$
	BEGIN

		DELETE FROM relay_groups
		WHERE 0 IN ( 
			SELECT COUNT(relay_group) from channels as c	
			WHERE c.relay_group = relay
		);

		RETURN (relay in (SELECT relay_group FROM relay_groups));

	END;
$function$
;
