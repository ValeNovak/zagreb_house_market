CREATE TABLE day_to_day_report (
        ID serial PRIMARY KEY,
        Date_of_reporting date default CURRENT_DATE,
        count_of_apartments_by_agencies int,
        count_of_apartments_by_private_seller int,
        median_price_of_apartment_by_agencies float,
        median_price_of_apartment_by_private_seller float,
        median_price_for_apartments_0_to_40_m2_zg float,
        median_price_for_apartments_40_to_80_m2_zg float,
        median_price_for_apartments_120_to_more_m2_zg float,
        count_of_energy_class_a_plus int,
        count_of_energy_class_a int,
        count_of_energy_class_b int,
        count_of_energy_class_c int,
        count_of_energy_class_d int,
        count_of_energy_class_e int,
        count_of_energy_class_f int,
        count_of_energy_class_g int,
        count_of_update_price_per_day int,
        count_of_update_price_increase_per_day int,
        count_of_update_price_decrease_per_day int
)

UPDATE day_to_day_report
set Date_of_reporting = '2025-03-27'
where id =2

select*from day_to_day_report

