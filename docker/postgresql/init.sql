DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = 'issue-db'
   ) THEN
      PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE "issue-db"');
   END IF;
END
$do$;
