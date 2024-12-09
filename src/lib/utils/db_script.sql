CREATE SCHEMA review_schema;

CREATE TABLE
  review_schema.reviews (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    review TEXT,
    sentiment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
  );

CREATE INDEX idx_reviews_review_fts ON review_schema.reviews USING gin(to_tsvector('russian', review));