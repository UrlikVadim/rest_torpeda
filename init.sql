-- Table: public.largetable

-- DROP TABLE IF EXISTS public.largetable;

CREATE TABLE IF NOT EXISTS public.largetable
(
    id bigint NOT NULL DEFAULT 'nextval('largetable_id_seq'::regclass)',
    text_f text COLLATE pg_catalog."default",
    number_f numeric,
    ts_f timestamp with time zone,
    bool_f boolean,
    CONSTRAINT largetable_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.largetable
    OWNER to admin;