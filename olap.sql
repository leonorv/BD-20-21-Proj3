/*Query 1*/
/*O ​ número de análises de glicémia ​ realizadas por especialidade médica, por mês e por ano, ​ com
totais parciais em cada especialidade cada mês e cada ano,​ em 2017-2020*/
select m.especialidade, dt.mes, dt.ano, count(*) from f_analise as fa
inner join Medico as m on m.num_cedula = fa.id_medico
inner join d_tempo as dt on fa.id_data_registo = dt.id_tempo
where fa.nome = 'Glicémia' and dt.ano between '2017' and '2020'
group by rollup(m.especialidade, dt.mes, dt.ano);

/*Query 2*/
/*A ​ quantidade total e ​ no médio de prescrições diário ​ de cada substância registados em cada dia
da semana, ​ cada mês e em cada concelho​ , ​ com rollup no espaço (concelho) e no tempo (dia da
semana e mês) num determinado trimestre e região, mostrando o resultado para a região de
Lisboa durante o 1o trimestre de 2020.*/
select fpv.substancia, c.nome, dt.mes, dt.dia_da_semana, sum(fpv.quant), 
avg(count_presc) from (
    select count(fpv.id_presc_venda) as count_presc from f_presc_venda as fpv
    inner join d_tempo as dt on dt.id_tempo = fpv.id_data_registo
    inner join d_instituicao as di on di.id_inst = fpv.id_inst
    inner join Concelho as c on di.num_concelho = c.num_concelho
    inner join Regiao as r on r.num_regiao = c.num_regiao
    where r.nome = 'Centro' and dt.trimestre = 3 and dt.ano = '2020'
) as average, f_presc_venda as fpv
inner join d_tempo as dt on dt.id_tempo = fpv.id_data_registo
inner join d_instituicao as di on di.id_inst = fpv.id_inst
inner join Concelho as c on di.num_concelho = c.num_concelho
inner join Regiao as r on r.num_regiao = c.num_regiao
where r.nome = 'Centro' and dt.trimestre = 3 and dt.ano = '2020'
group by fpv.substancia, rollup(c.nome, dt.mes, dt.dia_da_semana);

select distinct  
    product_line,
    category,
    round(avg(price),2) as avg_price    
  from catalog
  group by
    product_line,
    category
  order by product_line


select * from crosstab (  
  'select distinct
    product_line,
    category,
    round(avg(price),2) as avg_price    
  from catalog
  group by
    product_line,
    category
  order by product_line',

  'select distinct category from catalog order by 1'
 )
 AS (
   product_line character varying,
   dog_toys_avg_price numeric,
   dog_wear_avg_price numeric
 )
 ;
