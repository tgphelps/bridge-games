
create table if not exists Deals (
    session_id text not null,
    deal_id integer not null,
    viewer_link text not null,
    auction text,
    opening_lead text,
    primary key (session_id, deal_id)
);
