/*QUERY 1*/ 
select nome
from concelho c natural join instituicao i natural join venda_farmacia v
where v.data == current.date
group by num_concelho
having count(num_vendas) >= ALL
    (select count(num_vendas)
    from c natural join i natural join v
	where v.data == current.date
    group by num_concelho
    );


/*QUERY 2*/
select m.nome,
from medico as m natural join prescricao p natural join regiao r
where data between '2019-01-01 00:00:00' and '2019-06-30 23:59:59';
group by num_regiao
having count(data) >= ALL
    (select count(data) 
    from m natural join p natural join r
    where data between '2019-01-01 00:00:00' and '2019-06-30 23:59:59'
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
    from venda_farmacia v_f natural join prescricao_venda p_v
    natural join i natural join concelho c
    where m.num_cedula = p_v.num_cedula and v_f.substancia = 'Aspirina' and c.nome = 'Arouca'
    and v_f.data_registo between '2020-01-01 00:00:00' and '2020-12-31 23:59:59'
    );

/*QUERY 4*/
select distinct a.num_doente 
from analise a
where a.data_registo between '2020-11-01 00:00:00' and '2020-11-31 23:59:59'
and not exists (
    select * from venda_farmacia natural join prescricao_venda
    where a.num_doente = num_doente and data_registo between '2020-11-01 00:00:00' and '2020-11-31 23:59:59'
    );



    