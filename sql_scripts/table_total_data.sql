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