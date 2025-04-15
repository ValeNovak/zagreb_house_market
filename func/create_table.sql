
CREATE TABLE IF NOT EXISTS zagreb_app(
    Njuskalo_id BIGINT,
    Author text,
    "Naslov" text,
    "Cijena" float,
    "Stambena povrsina" float,
    "Netto povrsina" float,
    "Lokacija" text,
    "Broj soba" text,
    "Kat" text,
    "Godina izgradnje" int,
    "Tip stana" text,
    "Balkon/Loda/Terasa" text,
    "Broj etaze" text,
    "Broj parkirnih mjesta" int,
    "Energetski razred" text,
    "Oglas objavljen" date,
    "Oglas prikazan" int,
    PRIMARY KEY (Njuskalo_id, Author)
)



CREATE TABLE update_price(
    id serial PRIMARY KEY,
    Njuskalo_id BIGINT,
    Author text,
    Old_price float,
    New_price float,
    Date_of_UP DATE DEFAULT CURRENT_DATE
)




