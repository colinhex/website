SELECT column_name FROM information_schema.columns
WHERE table_schema = 'general'
AND table_name = %s;
