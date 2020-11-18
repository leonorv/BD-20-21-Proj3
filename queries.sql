/*QUERY 1*/ 
select nome
from concelho as c join instituicao as i join venda_farmacia as v
where v.data == current.date and c.num_concelho = i.num_concelho and i.nome = v.inst
group by num_concelho
having sum(preco) >= ALL
    (select sum(preco)
    from c natural join i natural join v
	where v.data == current.date
    group by num_concelho
    );


/*QUERY 2*/
select m.nome,
from consulta as c join instituicao as i join medico as m join prescricao as p join regiao as r
where data between '2019-1-1 00:00:00' and '2019-6-30 23:59:59' and c.num_cedula = m.num_cedula and c.inst = i.nome and i.num_regiao = r.num_regiao
group by num_regiao 
having count(data) >= ALL
    (select count(data) 
    from c join i join m join p join r
    where data between '2019-1-1 00:00:00' and '2019-6-30 23:59:59' and c.num_cedula = m.num_cedula and c.inst = i.nome and i.num_regiao = r.num_regiao
    );

/*QUERY 3*/
select m.nome
from medico as m
where not exists (
    select i.nome
    from instituicao i
    where i.tipo = 'Farmacia'
    except
    select i.nome
    from venda_farmacia as v_f join prescricao_venda as p_v join i join concelho c
    where m.num_cedula = p_v.num_cedula and v_f.substancia = 'Aspirina' and c.nome = 'Arouca' 
    and c.num_concelho = i.num_concelho and v_f.num_venda = p_v.num_venda 
    and v_f.data_registo between '2020-1-1 00:00:00' and '2020-12-31 23:59:59'
    );

/*QUERY 4*/
select distinct a.num_doente 
from analise as a
where a.data_registo between '2020-11-1 00:00:00' and '2020-11-31 23:59:59'
and not exists (
    select * from venda_farmacia as v_f join prescricao_venda as p_v
    where a.num_doente = num_doente and data_registo between '2020-11-01 00:00:00' and '2020-11-31 23:59:59' 
    and v_f.num_venda = p_v.num_venda
    );



    