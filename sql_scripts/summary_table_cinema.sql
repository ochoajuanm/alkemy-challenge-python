CREATE TABLE public.summary_table_cinema
(
    id integer NOT NULL,
    provincia character varying,
    butacas integer,
    espacio_incaa integer,
    pantallas integer,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.summary_table_cinema
    OWNER to postgres;