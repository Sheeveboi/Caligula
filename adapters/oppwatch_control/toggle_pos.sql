CREATE OR REPLACE FUNCTION toggle_pos(ign text) 
RETURNS INT 
LANGUAGE plpgsql
AS $$

BEGIN
	IF ign NOT IN (SELECT username FROM pos_igns) THEN
		
		INSERT INTO pos_igns (username) VALUES (ign);
		
	ELSE 
	
		DELETE FROM pos_igns WHERE username = ign;
		
	END IF;
	
	RETURN 0;
END;
$$;

SELECT toggle_pos(%s);