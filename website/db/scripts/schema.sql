




create table BlogPosts (
    bid integer primary key,
    author varchar(24) not null,
    pinned boolean not null default false,
    blog_text text not null,
    blog_date date not null
);