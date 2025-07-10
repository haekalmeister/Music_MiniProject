DROP TABLE IF EXISTS data;
DROP TABLE IF EXISTS data_reject;

CREATE TABLE data (
    dates DATE,
    ids VARCHAR PRIMARY KEY,
    names VARCHAR,
    monthly_listeners INTEGER,
    popularity INTEGER,
    followers INTEGER,
    genres VARCHAR[],
    first_release INTEGER,
    last_release INTEGER,
    num_releases INTEGER,
    num_tracks INTEGER,
    playlists_found VARCHAR,
    feat_track_ids VARCHAR[]
);

CREATE TABLE data_reject (
    dates DATE,
    ids VARCHAR,
    names VARCHAR,
    monthly_listeners INTEGER,
    popularity INTEGER,
    followers INTEGER,
    genres VARCHAR[],
    first_release INTEGER,
    last_release INTEGER,
    num_releases INTEGER,
    num_tracks INTEGER,
    playlists_found VARCHAR,
    feat_track_ids VARCHAR[]
);
