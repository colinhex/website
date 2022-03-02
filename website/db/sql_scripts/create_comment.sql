DO $$
declare id integer;
begin
insert into UpdateElements(element_author, element_date, element_text)
values (%s, %s, %s)
returning element_id into id;
insert into UpdateComments(element_id, parent_element_id)
values (id, %s);
end $$