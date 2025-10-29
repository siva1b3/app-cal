
CREATE TABLE IF NOT EXISTS public.operations
(
    operation_id SERIAL NOT NULL,
    operation_type character varying COLLATE pg_catalog."default",
    number_1 double precision,
    number_2 double precision,
    operation_result double precision,
    number_of_attempts integer NOT NULL DEFAULT 0,
    CONSTRAINT "PK_operations__operation_id" PRIMARY KEY (operation_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.operations
    OWNER to admin_user;
