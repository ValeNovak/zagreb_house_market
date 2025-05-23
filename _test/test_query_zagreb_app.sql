select * from zagreb_app

-- zagreb_app table test
select count(njuskalo_id) 
from zagreb_app


select* --- TEST QUERY FOR AGENCY
from zagreb_app
where author ilike '%nekretnine%' 
or author ilike '%nekretnina%'
or author ilike '%d.o.o%' 
or author ilike '%real%' 
or author ilike '%Immobilien%' 
or author ilike '%properties%'
or author ilike '%agencija%'
or author ilike '%projekt%'
or author ilike '%www%'



select* --------- QUERY FOR AGENCY
from zagreb_app z
where not EXISTS
(select*
from
(select* 
from zagreb_app
where author not ilike '%nekretnine%' 
and author not ilike '%nekretnina%'
and author not ilike '%d.o.o%' 
and author not ilike '%real%' 
and author not ilike '%Immobilien%' 
and author not ilike '%properties%'
and author not ilike '%agencija%'
and author not ilike '%projekt%'
and author not ilike '%www%'
and LEFT(author, 1) != UPPER(LEFT(author, 1))) as consumeri
where consumeri.author = z.author) and author !~ '\d+$' and author !~ '^[^A-Za-z0-9]'
ORDER BY author



---- QUERY FOR PRIVATE PERSON
SELECT *  
FROM zagreb_app
WHERE author not ilike '%nekretnine%' 
and author not ilike '%nekretnina%'
and author not ilike '%d.o.o%' 
and author not ilike '%real%' 
and author not ilike '%Immobilien%' 
and author not ilike '%properties%'
and author not ilike '%agencija%'
and author not ilike '%projekt%'
and author not ilike '%www%'
and LEFT(author, 1) != UPPER(LEFT(author, 1))


select AVG('Cijena')
from zagreb_app
where 'Stambena povrsina' > 120


SELECT 
    "author",
    "Naslov",
    "Lokacija",
    "Stambena povrsina",
    "Broj soba",
    "Kat",
    "Godina izgradnje",
    "Tip stana",
    COUNT(*) AS broj_ponavljanja
FROM zagreb_app
GROUP BY 
    "author",
    "Naslov",
    "Lokacija",
    "Stambena povrsina",
    "Broj soba",
    "Kat",
    "Godina izgradnje",
    "Tip stana"
HAVING COUNT(*) > 1
ORDER BY broj_ponavljanja DESC;


SELECT *
FROM zagreb_app
WHERE "Stambena povrsina" = (
    SELECT MAX("Stambena povrsina")
    FROM zagreb_app
);






