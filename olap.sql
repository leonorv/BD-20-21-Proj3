select count(*) from f_analise as a, d_tempo as dt
where a.nome = 'Glicémia' and a.id_data_registo = dt.id_tempo and dt.year between '2017' and '2020'