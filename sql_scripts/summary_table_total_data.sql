CREATE TABLE public.summary_table_total_data
(
    id integer NOT NULL,
    tipo_agrupacion character varying,
    descripcion character varying,
    total integer,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.summary_table_total_data
    OWNER to postgres;
