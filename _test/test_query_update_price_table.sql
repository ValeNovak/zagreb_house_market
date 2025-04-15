-- update_price table test
select * from update_price



select count(distinct(njuskalo_id))
from update_price



select u.njuskalo_id, u.author, u.old_cijena, u.new_cijena, z."Stambena povrsina", old_cijena-new_cijena as razlika
from update_price u
join zagreb_app z on u.njuskalo_id = z.njuskalo_id
where old_cijena > new_cijena and "Stambena povrsina" > 45.0
and new_cijena < 200000
