DO $$
declare id integer;
begin
insert into UpdateElements(element_author, element_date, element_text)
values (%s, %s, %s)
returning element_id into id;
insert into UpdatePosts(element_id, post_href, post_title)
values (id, %s, %s);
end $$