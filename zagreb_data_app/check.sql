SELECT * FROM zagreb_app


SELECT ROUND(AVG("Cijena" / "Netto povrsina")::numeric, 2)
FROM zagreb_app

SELECT ROUND(AVG("Cijena")::numeric, 2)
FROM zagreb_app

SELECT ROUND(AVG("Netto povrsina")::numeric, 2)
FROM zagreb_app

SELECT *
from update_price
where old_cijena > new_cijena