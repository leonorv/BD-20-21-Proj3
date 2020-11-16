/*QUERY 1*/ 
select nome
from concelho as c natural join instituicao as i natural join venda_farmacia as v
where v.data == current.date
group by num_concelho
having count(num_vendas) >= ALL
    (select count(num_vendas)
    from c natural join i natural join v
	where v.data == current.date
    group by num_concelho);


/*QUERY 2*/
select m.nome,
from medico as m natural join prescricao as p natural join regiao as r
where data between '2019-01-01 00:00:00' and '2019-06-30 23:59:59';
group by num_regiao
having count(data) >= ALL
    (select count(data) 
    from m natural join p natural join r
    where data between '2019-01-01 00:00:00' and '2019-06-30 23:59:59');

/*QUERY 3*/
select nome
from medico as m natural join



    