
/* Tables */

create table Users (
    user_id varchar(24),
    email bytea unique not null,
    email_confirmed boolean default false,
    password varchar(256) not null,
    register_date date not null,
    deletion_date date default null,
    privileges varchar(24) not null default 'default',

    primary key (user_id)
);

create table Subscriptions (
    subscription_id serial,
    start_date date not null,
    end_date date default null,

    primary key (subscription_id)
);

create table users_have_subscriptions (
    user_id varchar(64),
    subscription_id int,

    foreign key (subscription_id) references Subscriptions(subscription_id),
    foreign key (user_id) references Users(user_id),

    primary key (user_id, subscription_id)
);

create table Contacts (
    contact_no serial,
    email varchar(255) not null,
    first_name varchar(24) not null,
    last_name varchar(24) not null,
    organization varchar(24),
    contact_text text not null,
    contact_date date not null,

    primary key (contact_no)
);

create table PageVisits (
    visit_no serial,
    url varchar(64) not null,
    webclient varchar(24),
    ipv4 varchar(24),

    primary key (visit_no)
);

create table visits_correspond_with_logs (
    visit_no integer,
    log_no integer,

    foreign key (visit_no) references PageVisits(visit_no),
    foreign key (log_no) references ServerLogs(log_no),

    primary key (visit_no, log_no)
);

create table users_visit_pages (
    user_id varchar(24),
    visit_no integer,

    foreign key (user_id) references Users(user_id),
    foreign key (visit_no) references PageVisits(visit_no),

    primary key (user_id, visit_no)
);

create table ServerLogs (
    log_no serial primary key
    /*
    Todo: ServerLogs Table
    */
);

create table UpdateElements (
    element_id serial,
    element_author varchar(24),
    element_text text not null,
    element_date date not null,
    approved boolean not null default false,

    foreign key (element_author) references Users(user_id),

    primary key (element_id)
);


create table UpdatePosts (
    element_id integer,
    post_title varchar(24) not null,
    post_href varchar(24),
    pinned boolean not null default false,

    foreign key (element_id) references UpdateElements(element_id),

    primary key (element_id)
);

create table UpdateComments (
    element_id integer,
    parent_element_id integer,

    foreign key (element_id) references UpdateElements(element_id),
    foreign key (parent_element_id) references UpdateElements(element_id),

    primary key (element_id)
);


/* Additional Constraints */


/* Triggers */


/* Access Grants */


/* Views */

drop view posts;
drop view comments;

create view Posts as
    select
        ue.element_id,
        ue.element_author,
        ue.element_date,
        up.post_title,
        up.post_href,
        ue.element_text,
        up.pinned
    from UpdateElements ue, UpdatePosts up
    where ue.element_id = up.element_id;


create view Comments as
    select
        ue.element_id,
        ue.element_author,
        ue.element_date,
        uc.parent_element_id,
        ue.element_text
    from UpdateElements ue, UpdateComments uc
    where ue.element_id = uc.element_id;



