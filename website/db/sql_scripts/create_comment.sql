with ins as (
    insert into UpdateElements
    values (default, default, %s, %s, %s)
    returning element_id,
)
insert into UpdateComments
values (ins.element_id, %s);