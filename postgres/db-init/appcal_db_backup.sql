--
-- PostgreSQL database dump
--

\restrict xob82bIGVrJgLDjLxCHR3UI7FhWzVsYc34YFQc7UTbhfCoedbLhluNBoPRuGeHi

-- Dumped from database version 18.0 (Debian 18.0-1.pgdg13+3)
-- Dumped by pg_dump version 18.0 (Debian 18.0-1.pgdg13+3)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: operations; Type: TABLE; Schema: public; Owner: database_user
--

CREATE TABLE public.operations (
    operation_id bigint NOT NULL,
    operation_name character varying NOT NULL,
    number_1 integer NOT NULL,
    number_2 integer NOT NULL,
    result double precision,
    retry_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.operations OWNER TO database_user;

--
-- Name: operations_operation_id_seq; Type: SEQUENCE; Schema: public; Owner: database_user
--

CREATE SEQUENCE public.operations_operation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.operations_operation_id_seq OWNER TO database_user;

--
-- Name: operations_operation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: database_user
--

ALTER SEQUENCE public.operations_operation_id_seq OWNED BY public.operations.operation_id;


--
-- Name: operations operation_id; Type: DEFAULT; Schema: public; Owner: database_user
--

ALTER TABLE ONLY public.operations ALTER COLUMN operation_id SET DEFAULT nextval('public.operations_operation_id_seq'::regclass);


--
-- Data for Name: operations; Type: TABLE DATA; Schema: public; Owner: database_user
--

COPY public.operations (operation_id, operation_name, number_1, number_2, result, retry_count) FROM stdin;
\.


--
-- Name: operations_operation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: database_user
--

SELECT pg_catalog.setval('public.operations_operation_id_seq', 1, false);


--
-- Name: operations operations_pkey; Type: CONSTRAINT; Schema: public; Owner: database_user
--

ALTER TABLE ONLY public.operations
    ADD CONSTRAINT operations_pkey PRIMARY KEY (operation_id);


--
-- PostgreSQL database dump complete
--

\unrestrict xob82bIGVrJgLDjLxCHR3UI7FhWzVsYc34YFQc7UTbhfCoedbLhluNBoPRuGeHi

