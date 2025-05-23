-- update_price table test
select * from update_price



select count(distinct(njuskalo_id))
from update_price



select u.njuskalo_id, u.author, u.old_price, u.new_price, z."Stambena povrsina", old_price-new_price as razlika
from update_price u
join zagreb_app z on u.njuskalo_id = z.njuskalo_id
where old_price > new_price and "Stambena povrsina" > 45.0
and new_price < 200000
and (
        "Lokacija" ILIKE '%Trešnjevka - Jug%' OR
        "Lokacija" ILIKE '%Trešnjevka - Sjever%' OR
        "Lokacija" ILIKE '%Stenjevec%' OR
        "Lokacija" ILIKE '%Novi Zagreb - Zapad%'
    )



