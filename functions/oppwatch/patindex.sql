-- DROP FUNCTION public.patindex(varchar, varchar);

CREATE OR REPLACE FUNCTION public.patindex(pattern character varying, expression character varying)
 RETURNS integer
 LANGUAGE sql
 IMMUTABLE
AS $function$
SELECT
    COALESCE(
        STRPOS(
             $2
            ,(
                SELECT
                    ( REGEXP_MATCHES(
                        $2
                        ,'(' || REPLACE( REPLACE( TRIM( $1, '%' ), '%', '.*?' ), '_', '.' ) || ')'
                        ,'i'
                    ) )[ 1 ]
                LIMIT 1
            )
        )
        ,0
    )
;
$function$
;
