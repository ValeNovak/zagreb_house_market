ALTER TABLE zagreb_app   -- adding column
add column Naslov text  




select * from zagreb_app where njuskalo_id = 46470597

select * from njuskalo_attributes

select count(njuskalo_id) 
from zagreb_app







-- test insert for update/insert code
INSERT INTO zagreb_app (
    njuskalo_id, 
    author, 
    "Naslov", 
    "Balkon/Loda/Terasa", 
    "Broj etaze", 
    "Broj parkirnih mjesta", 
    "Broj soba", 
    "Cijena", 
    "Energetski razred", 
    "Godina izgradnje", 
    "Kat", 
    "Lokacija", 
    "Netto povrsina", 
    "Oglas objavljen", 
    "Oglas prikazan", 
    "Stambena povrsina", 
    "Tip stana"
) 
VALUES (
    33995792, 
    'K2 nekretnine', 
    'Gajnice, 4-sobni stan u urbanoj vili, 173, 42 m2 + garaža 30 m2 + VPM', 
    'Terasa, Balkon', 
    'Jednoetažni', 
    2, 
    '3-sobni', 
    43000, 
    'A', 
    2015, 
    -1, 
    'Grad Zagreb, Podsused - Vrapče, Gajnice', 
    173.42, 
    NULL,  -- Oglas objavljen je NULL
    9925, 
    173.42, 
    'U stambenoj zgradi'
);

CREATE TABLE if not EXISTS update_price(id serial PRIMARY KEY,
                                        njuskalo_id BIGINT NOT NULL, 
                                        "author" text, 
                                        old_cijena float, 
                                        new_cijena float,
                                        datum_promjene date default CURRENT_DATE 
                                        )

drop table update_price

select*from update_price


select count(njuskalo_id), njuskalo_id, author, old_cijena, new_cijena
from update_price
group by njuskalo_id, author, old_cijena, new_cijena

select njuskalo_id, author, datum_promjene
from update_price



DELETE FROM update_price a
USING update_price b
WHERE a.id > b.id
AND a.njuskalo_id = b.njuskalo_id
AND a.author = b.author
AND a.datum_promjene = b.datum_promjene;


WITH sorted AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS new_id
    FROM update_price
)
UPDATE update_price
SET id = sorted.new_id
FROM sorted
WHERE update_price.id = sorted.id;


