select count(*) from f_analise as a, d_tempo as dt
where a.nome = 'Glicémia' and a.id_data_registo = dt.id_tempo and dt.ano between '2017' and '2020'

especialidade | ano | mes | n_glicemica |
------------+-----------+------------+----
urologia      |2019 |   2 |         1
urologia |     2020 |   3 |         2   |                         
cardiologia |         4 |          2 |               6 |                               
cardiologia |         5 |          4 |               8 |      


select m.especialidade, fa.ano, fa.mes, count(*) from f_analise as fa
inner join Medico as m on m.num_cedula = fa.id_medico
inner join d_tempo as dt
where fa.nome = 'Glicémia' and fa.id_data_registo = dt.id_tempo and dt.ano between '2017' and '2020'
group by m.especialidade, fa.ano, fa.mes  


