CREATE TABLE public.total_data
(
    id integer NOT NULL,
    cod_loc integer,
    idprovincia integer,
    iddepartamento integer,
    categoria character varying,
    provincia character varying,
    localidad character varying,
    nombre character varying,
    direccion character varying,
    telefono character varying,
    mail character varying,
    fuente character varying,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.total_data
    OWNER to postgres;

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