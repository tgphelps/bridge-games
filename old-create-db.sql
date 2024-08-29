
create table if not exists Deals (
    session_id text not null,
    deal_id integer not null,
    name_north text,
    name_south text,
    name_east text,
    name_west text,
    dealer text not null,
    vuln text not null,
    hand_north text not null,
    hand_south text not null,
    hand_east text not null,
    hand_west text not null,
    auction text,
    contract text not null,
    declarer text not null,
    opening_lead text,
    primary key (session_id, deal_id)
);
