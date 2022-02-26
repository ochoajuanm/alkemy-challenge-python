CREATE TABLE public.summary_table_total_data
(
    tipo_agrupacion character varying,
    descripcion character varying,
    total integer,
    creado_el timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE IF EXISTS public.summary_table_total_data
    OWNER to postgres;