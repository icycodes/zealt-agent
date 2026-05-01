CREATE TABLE IF NOT EXISTS test_migration (id UInt64) ENGINE = MergeTree ORDER BY id;
ALTER TABLE test_migration ADD COLUMN IF NOT EXISTS name String;
