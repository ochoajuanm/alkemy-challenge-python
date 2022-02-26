CREATE TABLE public.total_data
(
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
    web character varying,
    creado_el timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE IF EXISTS public.total_data
    OWNER to postgres;