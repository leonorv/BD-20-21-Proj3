/*QUERY 1*/ 
select nome
from concelho as c natural join instituicao as i natural join venda_farmacia as v
where v.data == current.date
group by num_concelho
having count(num_vendas) >= ALL
    (select count(num_vendas)
    from c natural join i natural join v
	where v.data == current.date
    group by num_concelho)




    