CREATE TABLE public.summary_table_cinema
(
    provincia character varying,
    butacas integer,
    espacio_incaa integer,
    pantallas integer,
    creado_el timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE IF EXISTS public.summary_table_cinema
    OWNER to postgres;