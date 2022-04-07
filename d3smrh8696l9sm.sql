-- Adminer 4.8.1 PostgreSQL 14.2 (Ubuntu 14.2-1.pgdg20.04+1) dump

DROP TABLE IF EXISTS "accidents2017";
CREATE TABLE "public"."accidents2017" (
    "incident_info" text NOT NULL,
    "description" text NOT NULL,
    "start_dt" text NOT NULL,
    "modified_dt" text NOT NULL,
    "quadrant" text NOT NULL,
    "longitude" text NOT NULL,
    "latitude" text NOT NULL
) WITH (oids = false);


DROP TABLE IF EXISTS "updates";
DROP SEQUENCE IF EXISTS updates_update_id_seq;
CREATE SEQUENCE updates_update_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."updates" (
    "update_user" text NOT NULL,
    "comments" text NOT NULL,
    "update_id" integer DEFAULT nextval('updates_update_id_seq') NOT NULL,
    "update_time" timestamp NOT NULL,
    "update_location" text NOT NULL,
    CONSTRAINT "updates_pkey" PRIMARY KEY ("update_id")
) WITH (oids = false);


DROP TABLE IF EXISTS "users";
DROP SEQUENCE IF EXISTS users_user_id_seq;
CREATE SEQUENCE users_user_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."users" (
    "username" text NOT NULL,
    "password" text NOT NULL,
    "user_id" integer DEFAULT nextval('users_user_id_seq') NOT NULL,
    CONSTRAINT "users_pkey" PRIMARY KEY ("user_id")
) WITH (oids = false);


-- 2022-04-07 10:49:10.372645+00
