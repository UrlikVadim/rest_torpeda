-- Table: public.largetable

-- DROP TABLE IF EXISTS public.largetable;

CREATE TABLE IF NOT EXISTS public.largetable
(
    id bigserial NOT NULL,
    text_f text,
    number_f numeric,
    ts_f timestamp with time zone,
    bool_f boolean,
    CONSTRAINT largetable_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.largetable
    OWNER to test;