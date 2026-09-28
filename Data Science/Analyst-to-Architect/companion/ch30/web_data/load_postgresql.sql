-- Load Riverstone's website data into PostgreSQL. Create the database first: CREATE DATABASE riverstone_web;
DROP TABLE IF EXISTS web_events, ab_test_assignments, web_sessions;
CREATE TABLE web_sessions (
    session_id INTEGER PRIMARY KEY, visitor_id VARCHAR(12) NOT NULL, started_at TIMESTAMP NOT NULL,
    device VARCHAR(10) NOT NULL, browser VARCHAR(10) NOT NULL, channel VARCHAR(10) NOT NULL,
    region VARCHAR(10) NOT NULL, landing_page VARCHAR(40) NOT NULL, pages_viewed INTEGER NOT NULL,
    duration_seconds INTEGER NOT NULL, enquiry_submitted BOOLEAN NOT NULL, enquiry_value NUMERIC(12,2));
CREATE TABLE ab_test_assignments (
    visitor_id VARCHAR(12) NOT NULL, test_name VARCHAR(40) NOT NULL, variant VARCHAR(12) NOT NULL,
    assigned_at TIMESTAMP NOT NULL, PRIMARY KEY (visitor_id, test_name));
CREATE TABLE web_events (
    event_id INTEGER PRIMARY KEY, session_id INTEGER NOT NULL REFERENCES web_sessions(session_id),
    event_time TIMESTAMP NOT NULL, event_name VARCHAR(20) NOT NULL);
\copy web_sessions FROM 'web_data/web_sessions.csv' CSV HEADER NULL ''
\copy ab_test_assignments FROM 'web_data/ab_test_assignments.csv' CSV HEADER
\copy web_events FROM 'web_data/web_events.csv' CSV HEADER
CREATE INDEX idx_web_sessions_visitor ON web_sessions (visitor_id);
CREATE INDEX idx_web_events_session ON web_events (session_id);
ANALYZE;
