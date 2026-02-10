
CREATE SEQUENCE IF NOT EXISTS webftp.webftp_files_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

    
CREATE TABLE IF NOT EXISTS webftp.webftp_files
(
    id bigint NOT NULL DEFAULT nextval('webftp.webftp_files_id_seq'::regclass),
    file character varying(100) COLLATE pg_catalog."default" NOT NULL,
    alias character varying(255) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default" NOT NULL,
    original_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    extension character varying(50) COLLATE pg_catalog."default" NOT NULL,
    content_type character varying(255) COLLATE pg_catalog."default" NOT NULL,
    size bigint,
    allowed_usernames text COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    CONSTRAINT webftp_files_pkey PRIMARY KEY (id)
)