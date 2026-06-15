FROM postgres:17

COPY init.sql /docker-entrypoint-initdb.d/01_init.sql
COPY dump_clean.sql /docker-entrypoint-initdb.d/02_dump.sql