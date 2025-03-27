ALTER TABLE zagreb_app   -- adding column
add column Naslov text  




  where njuskalo_id = 46470597

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


-- creating and training for update_price table

CREATE TABLE if not EXISTS update_price(id serial PRIMARY KEY,
                                        njuskalo_id BIGINT NOT NULL, 
                                        "author" text, 
                                        old_cijena float, 
                                        new_cijena float,
                                        datum_promjene date default CURRENT_DATE 
                                        )

drop table update_price

select count(distinct(njuskalo_id))
from update_price

select * from update_price




select count(njuskalo_id), njuskalo_id, author, old_cijena, new_cijena
from update_price
group by njuskalo_id, author, old_cijena, new_cijena

select njuskalo_id, author, datum_promjene
from update_price

delete from update_price


select u.njuskalo_id, u.author, u.old_cijena, u.new_cijena, z."Stambena povrsina", old_cijena-new_cijena as razlika
from update_price u
join zagreb_app z on u.njuskalo_id = z.njuskalo_id
where old_cijena < new_cijena and "Stambena povrsina" > 45.0














-- for training pivot table

CREATE TABLE BMI (id_per BIGINT,
                atribut_name text,
                value_atr_text text,
                value_atr_float float,
                value_atr_int int
                )

drop table BMI


INSERT INTO BMI values (1, 'ime', 'Mario', NULL, NULL);
INSERT INTO BMI values (1, 'prezime', 'Marić', NULL, NULL);
INSERT INTO BMI values (1, 'godine', NULL, NULL, 34);
INSERT INTO BMI values (1, 'tezina', NULL, 89.5, NULL);
INSERT INTO BMI values (1, 'visina', NULL, 172.3, NULL);

INSERT INTO BMI values (2, 'ime', 'Ivana', NULL, NULL);
INSERT INTO BMI values (2, 'prezime', 'Horvat', NULL, NULL);
INSERT INTO BMI values (2, 'godine', NULL, NULL, 28);
INSERT INTO BMI values (2, 'tezina', NULL, 65.2, NULL);
INSERT INTO BMI values (2, 'visina', NULL, 168.7, NULL);

INSERT INTO BMI values (3, 'ime', 'Marko', NULL, NULL);
INSERT INTO BMI values (3, 'prezime', 'Kovač', NULL, NULL);
INSERT INTO BMI values (3, 'godine', NULL, NULL, 40);
INSERT INTO BMI values (3, 'tezina', NULL, 92.8, NULL);
INSERT INTO BMI values (3, 'visina', NULL, 180.5, NULL);




select * from BMI


