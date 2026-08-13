-- Automated nightly backup
-- Host: db-prod-01.internal.skyblue.com
-- Generated: 2026-08-01 03:00:12 UTC
-- WARNING: internal use only, do not distribute

CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(64),
    email VARCHAR(128),
    password_hash VARCHAR(256),
    role VARCHAR(32),
    created_at DATETIME
);

INSERT INTO users (id, username, email, password_hash, role, created_at) VALUES
(1, 'admin', 'admin@skyblue.com', '$2b$12$KIXQ8Z5examplehash0000000000000000000001', 'superadmin', '2024-01-15 09:12:00'),
(2, 'jsmith', 'j.smith@skyblue.com', '$2b$12$KIXQ8Z5examplehash0000000000000000000002', 'staff', '2024-02-03 14:22:11'),
(3, 'svc_backup', 'svc-backup@skyblue.com', '$2b$12$KIXQ8Z5examplehash0000000000000000000003', 'service', '2024-01-15 09:15:00');

CREATE TABLE api_keys (
    id INT PRIMARY KEY,
    service_name VARCHAR(64),
    key_value VARCHAR(128),
    environment VARCHAR(16)
);

INSERT INTO api_keys (id, service_name, key_value, environment) VALUES
(1, 'payment-gateway', 'sk_live_0000000000000000000000EXAMPLE', 'production'),
(2, 'internal-monitoring', 'mon_key_EXAMPLE0000000000000000', 'production');

-- End of dump
