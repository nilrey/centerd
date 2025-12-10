--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.10
-- Dumped by pg_dump version 9.6.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: webmail; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA webmail;


ALTER SCHEMA webmail OWNER TO postgres;

--
-- Name: SCHEMA webmail; Type: MAC LABEL; Schema: -; Owner: postgres
--

MAC LABEL ON SCHEMA webmail IS '{0,0}';


--
-- Name: SCHEMA webmail; Type: MAC CCR; Schema: -; Owner: postgres
--

MAC CCR ON SCHEMA webmail IS ON;


--
-- Name: seq_webmail_dir_id; Type: SEQUENCE; Schema: webmail; Owner: postgres
--

CREATE SEQUENCE webmail.seq_webmail_dir_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE webmail.seq_webmail_dir_id OWNER TO postgres;

--
-- Name: SEQUENCE seq_webmail_dir_id; Type: MAC LABEL; Schema: webmail; Owner: postgres
--

MAC LABEL ON SEQUENCE webmail.seq_webmail_dir_id IS '{0,0}';


--
-- Name: SEQUENCE seq_webmail_dir_id; Type: MAC CCR; Schema: webmail; Owner: postgres
--

MAC CCR ON SEQUENCE webmail.seq_webmail_dir_id IS ON;


--
-- Name: seq_webmail_file_id; Type: SEQUENCE; Schema: webmail; Owner: postgres
--

CREATE SEQUENCE webmail.seq_webmail_file_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE webmail.seq_webmail_file_id OWNER TO postgres;

--
-- Name: SEQUENCE seq_webmail_file_id; Type: MAC LABEL; Schema: webmail; Owner: postgres
--

MAC LABEL ON SEQUENCE webmail.seq_webmail_file_id IS '{0,0}';


--
-- Name: SEQUENCE seq_webmail_file_id; Type: MAC CCR; Schema: webmail; Owner: postgres
--

MAC CCR ON SEQUENCE webmail.seq_webmail_file_id IS ON;


--
-- Name: seq_webmail_message_id; Type: SEQUENCE; Schema: webmail; Owner: postgres
--

CREATE SEQUENCE webmail.seq_webmail_message_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE webmail.seq_webmail_message_id OWNER TO postgres;

--
-- Name: SEQUENCE seq_webmail_message_id; Type: MAC LABEL; Schema: webmail; Owner: postgres
--

MAC LABEL ON SEQUENCE webmail.seq_webmail_message_id IS '{0,0}';


--
-- Name: SEQUENCE seq_webmail_message_id; Type: MAC CCR; Schema: webmail; Owner: postgres
--

MAC CCR ON SEQUENCE webmail.seq_webmail_message_id IS ON;


--
-- Name: seq_webmail_msg_recieved_id; Type: SEQUENCE; Schema: webmail; Owner: postgres
--

CREATE SEQUENCE webmail.seq_webmail_msg_recieved_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE webmail.seq_webmail_msg_recieved_id OWNER TO postgres;

--
-- Name: SEQUENCE seq_webmail_msg_recieved_id; Type: MAC LABEL; Schema: webmail; Owner: postgres
--

MAC LABEL ON SEQUENCE webmail.seq_webmail_msg_recieved_id IS '{0,0}';


--
-- Name: SEQUENCE seq_webmail_msg_recieved_id; Type: MAC CCR; Schema: webmail; Owner: postgres
--

MAC CCR ON SEQUENCE webmail.seq_webmail_msg_recieved_id IS ON;


--
-- Name: seq_webmail_msg_sent_id; Type: SEQUENCE; Schema: webmail; Owner: postgres
--

CREATE SEQUENCE webmail.seq_webmail_msg_sent_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE webmail.seq_webmail_msg_sent_id OWNER TO postgres;

--
-- Name: SEQUENCE seq_webmail_msg_sent_id; Type: MAC LABEL; Schema: webmail; Owner: postgres
--

MAC LABEL ON SEQUENCE webmail.seq_webmail_msg_sent_id IS '{0,0}';


--
-- Name: SEQUENCE seq_webmail_msg_sent_id; Type: MAC CCR; Schema: webmail; Owner: postgres
--

MAC CCR ON SEQUENCE webmail.seq_webmail_msg_sent_id IS ON;


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: webmail_dir; Type: TABLE; Schema: webmail; Owner: postgres
--

CREATE TABLE webmail.webmail_dir (
    id integer DEFAULT nextval('webmail.seq_webmail_dir_id'::regclass) NOT NULL,
    user_id integer NOT NULL,
    parent_id integer DEFAULT 0,
    title character varying(255) NOT NULL,
    description text,
    sort integer DEFAULT 0,
    created timestamp without time zone DEFAULT date_trunc('second'::text, now()) NOT NULL,
    modified timestamp without time zone DEFAULT date_trunc('second'::text, now()) NOT NULL
)
WITH (MACS=FALSE);


ALTER TABLE webmail.webmail_dir OWNER TO postgres;

--
-- Name: TABLE webmail_dir; Type: MAC LABEL; Schema: webmail; Owner: postgres
--

MAC LABEL ON TABLE webmail.webmail_dir IS '{0,0}';


--
-- Name: TABLE webmail_dir; Type: MAC CCR; Schema: webmail; Owner: postgres
--

MAC CCR ON TABLE webmail.webmail_dir IS ON;


--
-- Name: webmail_file; Type: TABLE; Schema: webmail; Owner: postgres
--

CREATE TABLE webmail.webmail_file (
    id integer DEFAULT nextval('webmail.seq_webmail_file_id'::regclass) NOT NULL,
    msg_id integer NOT NULL,
    name_orig character varying(255) NOT NULL,
    name_hash character varying(32) NOT NULL,
    title text,
    content_type character varying(255),
    ext character varying(10),
    size integer,
    description text
)
WITH (MACS=FALSE);


ALTER TABLE webmail.webmail_file OWNER TO postgres;

--
-- Name: TABLE webmail_file; Type: MAC LABEL; Schema: webmail; Owner: postgres
--

MAC LABEL ON TABLE webmail.webmail_file IS '{0,0}';


--
-- Name: TABLE webmail_file; Type: MAC CCR; Schema: webmail; Owner: postgres
--

MAC CCR ON TABLE webmail.webmail_file IS ON;


--
-- Name: webmail_message; Type: TABLE; Schema: webmail; Owner: postgres
--

CREATE TABLE webmail.webmail_message (
    id integer DEFAULT nextval('webmail.seq_webmail_message_id'::regclass) NOT NULL,
    hash character varying(32) NOT NULL,
    msg_subj text,
    msg_text text,
    msg_status text,
    msg_date character(32),
    msg_from text,
    msg_to text,
    modified timestamp without time zone DEFAULT date_trunc('second'::text, now()) NOT NULL,
    cnt_files integer DEFAULT 0
)
WITH (MACS=FALSE);


ALTER TABLE webmail.webmail_message OWNER TO postgres;

--
-- Name: TABLE webmail_message; Type: MAC LABEL; Schema: webmail; Owner: postgres
--

MAC LABEL ON TABLE webmail.webmail_message IS '{0,0}';


--
-- Name: TABLE webmail_message; Type: MAC CCR; Schema: webmail; Owner: postgres
--

MAC CCR ON TABLE webmail.webmail_message IS ON;


--
-- Name: webmail_msg_recieved; Type: TABLE; Schema: webmail; Owner: postgres
--

CREATE TABLE webmail.webmail_msg_recieved (
    id integer DEFAULT nextval('webmail.seq_webmail_msg_recieved_id'::regclass) NOT NULL,
    msg_id integer NOT NULL,
    email_to text,
    important boolean DEFAULT false,
    status text,
    modified timestamp without time zone DEFAULT date_trunc('second'::text, now()) NOT NULL
)
WITH (MACS=FALSE);


ALTER TABLE webmail.webmail_msg_recieved OWNER TO postgres;

--
-- Name: TABLE webmail_msg_recieved; Type: MAC LABEL; Schema: webmail; Owner: postgres
--

MAC LABEL ON TABLE webmail.webmail_msg_recieved IS '{0,0}';


--
-- Name: TABLE webmail_msg_recieved; Type: MAC CCR; Schema: webmail; Owner: postgres
--

MAC CCR ON TABLE webmail.webmail_msg_recieved IS ON;


--
-- Name: webmail_msg_sent; Type: TABLE; Schema: webmail; Owner: postgres
--

CREATE TABLE webmail.webmail_msg_sent (
    id integer DEFAULT nextval('webmail.seq_webmail_msg_sent_id'::regclass) NOT NULL,
    msg_id integer NOT NULL,
    email_from text,
    important boolean DEFAULT false,
    status text,
    modified timestamp without time zone DEFAULT date_trunc('second'::text, now()) NOT NULL
)
WITH (MACS=FALSE);


ALTER TABLE webmail.webmail_msg_sent OWNER TO postgres;

--
-- Name: TABLE webmail_msg_sent; Type: MAC LABEL; Schema: webmail; Owner: postgres
--

MAC LABEL ON TABLE webmail.webmail_msg_sent IS '{0,0}';


--
-- Name: TABLE webmail_msg_sent; Type: MAC CCR; Schema: webmail; Owner: postgres
--

MAC CCR ON TABLE webmail.webmail_msg_sent IS ON;


--
-- Name: seq_webmail_dir_id; Type: SEQUENCE SET; Schema: webmail; Owner: postgres
--

SELECT pg_catalog.setval('webmail.seq_webmail_dir_id', 1, false);


--
-- Name: seq_webmail_file_id; Type: SEQUENCE SET; Schema: webmail; Owner: postgres
--

SELECT pg_catalog.setval('webmail.seq_webmail_file_id', 1, false);


--
-- Name: seq_webmail_message_id; Type: SEQUENCE SET; Schema: webmail; Owner: postgres
--

SELECT pg_catalog.setval('webmail.seq_webmail_message_id', 4, true);


--
-- Name: seq_webmail_msg_recieved_id; Type: SEQUENCE SET; Schema: webmail; Owner: postgres
--

SELECT pg_catalog.setval('webmail.seq_webmail_msg_recieved_id', 4, true);


--
-- Name: seq_webmail_msg_sent_id; Type: SEQUENCE SET; Schema: webmail; Owner: postgres
--

SELECT pg_catalog.setval('webmail.seq_webmail_msg_sent_id', 4, true);


--
-- Data for Name: webmail_dir; Type: TABLE DATA; Schema: webmail; Owner: postgres
--



--
-- Data for Name: webmail_file; Type: TABLE DATA; Schema: webmail; Owner: postgres
--



--
-- Data for Name: webmail_message; Type: TABLE DATA; Schema: webmail; Owner: postgres
--

INSERT INTO webmail.webmail_message (id, hash, msg_subj, msg_text, msg_status, msg_date, msg_from, msg_to, modified, cnt_files) VALUES (1, 'd5f9e67745ed86bcbd07b00cab431513', 'test', 'test', 'sent', '19-12-2023 11:54:45             ', 'citis@ncuo-portal.local', 'citis', '2023-12-19 11:54:50', 0);
INSERT INTO webmail.webmail_message (id, hash, msg_subj, msg_text, msg_status, msg_date, msg_from, msg_to, modified, cnt_files) VALUES (2, 'e657e9e9518b8d696aca998327be79d2', 'test2', 'test2', 'sent', '19-12-2023 12:05:11             ', 'lu2@ncuo-portal.local', 'lu1', '2023-12-19 12:05:16', 0);
INSERT INTO webmail.webmail_message (id, hash, msg_subj, msg_text, msg_status, msg_date, msg_from, msg_to, modified, cnt_files) VALUES (3, 'd3e9b110f17ceb1d64d24c9592fefbcb', 'test3', 'test3', 'sent', '19-12-2023 12:06:28             ', 'lu1@ncuo-portal.local', 'lu1', '2023-12-19 12:06:37', 0);
INSERT INTO webmail.webmail_message (id, hash, msg_subj, msg_text, msg_status, msg_date, msg_from, msg_to, modified, cnt_files) VALUES (4, '3e0d46c9a7e7f4a441005f7693694c48', 'test4', 'test4', 'sent', '19-12-2023 12:07:30             ', 'lu1@ncuo-portal.local', 'lu1@ncuo-portal.local', '2023-12-19 12:07:34', 0);


--
-- Data for Name: webmail_msg_recieved; Type: TABLE DATA; Schema: webmail; Owner: postgres
--

INSERT INTO webmail.webmail_msg_recieved (id, msg_id, email_to, important, status, modified) VALUES (1, 1, 'citis', false, 'undelivered', '2023-12-19 11:54:45');
INSERT INTO webmail.webmail_msg_recieved (id, msg_id, email_to, important, status, modified) VALUES (2, 2, 'lu1', false, 'undelivered', '2023-12-19 12:05:11');
INSERT INTO webmail.webmail_msg_recieved (id, msg_id, email_to, important, status, modified) VALUES (3, 3, 'lu1', false, 'undelivered', '2023-12-19 12:06:28');
INSERT INTO webmail.webmail_msg_recieved (id, msg_id, email_to, important, status, modified) VALUES (4, 4, 'lu1@ncuo-portal.local', false, 'undelivered', '2023-12-19 12:07:30');


--
-- Data for Name: webmail_msg_sent; Type: TABLE DATA; Schema: webmail; Owner: postgres
--

INSERT INTO webmail.webmail_msg_sent (id, msg_id, email_from, important, status, modified) VALUES (1, 1, 'citis@ncuo-portal.local', false, 'sent', '2023-12-19 11:54:45');
INSERT INTO webmail.webmail_msg_sent (id, msg_id, email_from, important, status, modified) VALUES (2, 2, 'lu2@ncuo-portal.local', false, 'sent', '2023-12-19 12:05:11');
INSERT INTO webmail.webmail_msg_sent (id, msg_id, email_from, important, status, modified) VALUES (3, 3, 'lu1@ncuo-portal.local', false, 'sent', '2023-12-19 12:06:28');
INSERT INTO webmail.webmail_msg_sent (id, msg_id, email_from, important, status, modified) VALUES (4, 4, 'lu1@ncuo-portal.local', false, 'sent', '2023-12-19 12:07:30');


--
-- PostgreSQL database dump complete
--

