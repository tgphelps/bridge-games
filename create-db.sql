
create table if not exists Deals (
    session text not null,
    board integer not null,
    viewer_link text not null,
    dealer text,
    auction text,
    opening_lead text,
    result integer,
    match_points real,
    max_points real,
    primary key (session, board)
);
