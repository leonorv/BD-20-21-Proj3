/*especialidade | ano | mes | n_glicemica |
----------------+-----+-----+-------------+
urologia        |2019 |  2  |      1      |
urologia        |2020 |  3  |      2      |                         
cardiologia     |2017 |  4  |      2      |                                
cardiologia     |2018 |  5  |      4      |      */      

/*Query 1*/
select m.especialidade, dt.ano, dt.mes, count(*) from f_analise as fa
inner join Medico as m on m.num_cedula = fa.id_medico
inner join d_tempo as dt on fa.id_data_registo = dt.id_tempo
where fa.nome = 'Glicémia' and dt.ano between '2017' and '2020'
group by m.especialidade, dt.ano, dt.mes;

/*Query 2*/


