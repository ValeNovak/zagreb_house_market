CREATE EXTENSION IF NOT EXISTS tablefunc;

SELECT * FROM crosstab(
    'SELECT id_per, atribut_name, 
            COALESCE(value_atr_text, 
                CAST(value_atr_float as TEXT), 
                CAST(value_atr_int as TEXT)) as value
     FROM BMI 
     ORDER BY id_per'
) AS pivot_table (id_per BIGINT, ime TEXT, prezime TEXT, godine TEXT, tezina TEXT, visina TEXT);



SELECT id_per, atribut_name, 
            COALESCE(value_atr_text, 
                CAST(value_atr_float as TEXT), 
                CAST(value_atr_int as TEXT)) as value
     FROM BMI 
     ORDER BY id_per