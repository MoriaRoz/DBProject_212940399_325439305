UPDATE Event
SET Location = 'Tel Aviv'
WHERE Event_id = 2;

rollback;

UPDATE Event
SET Location = 'Tel Aviv'
WHERE Event_id = 2;

commit;
