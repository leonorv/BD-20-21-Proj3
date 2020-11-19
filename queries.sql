/*QUERY 1*/ 
select c.nome
from concelho as c, instituicao as i, vendafarmacia as v
where date(v.data_registo) = current_date and c.num_concelho = i.num_concelho and i.nome = v.inst
group by c.nome
having sum(preco) >= ALL
    (select sum(v.preco)
    from concelho as c, instituicao as i, vendafarmacia as v
	where date(v.data_registo) = current_date and i.nome = v.inst and i.num_concelho = c.num_concelho
    group by c.nome
    );


/*QUERY 2*/
select r.nome, m.nome
from consulta as c, prescricao as p, instituicao as i, medico as m, regiao as r
where c.num_cedula = p.num_cedula and c.num_doente = p.num_doente and c.dia_hora = p.dia_hora and
p.dia_hora between '2019-1-1 00:00:00' and '2019-6-30 23:59:59' and p.num_cedula = m.num_cedula and c.nome_instituicao = i.nome and i.num_regiao = r.num_regiao
group by r.num_regiao, m.nome
having count(p.dia_hora) >= ALL
    (select count(p.dia_hora) 
    from consulta as c natural join prescricao as p, instituicao as i, medico as m, regiao as r
    where p.dia_hora between '2019-1-1 00:00:00' and '2019-6-30 23:59:59' and p.num_cedula = m.num_cedula and c.nome_instituicao = i.nome and i.num_regiao = r.num_regiao
    group by r.num_regiao, m.nome
    );

/*QUERY 3*/
select distinct m.nome
from prescricaovenda as p_v, medico as m, vendafarmacia as v_f, instituicao as i,concelho as c
where p_v.num_cedula = m.num_cedula and p_v.num_venda = v_f.num_venda and 
v_f.inst = i.nome and i.num_concelho = c.num_concelho and c.nome = 'Arouca' and i.tipo = 'farmacia'
group by m.nome
having count(p_v.num_venda) = (
    select count(i.nome)
    from instituicao as i, concelho as c
    where c.nome = 'Arouca' and i.num_concelho = c.num_concelho and i.tipo = 'farmacia'
);

/*QUERY 4*/
select distinct a.num_doente 
from analise as a
where extract(year from a.data_registo) = extract(year from current_date) and
extract(month from a.data_registo) = extract(month from current_date)
and not exists (
    select * from venda_farmacia as v_f, prescricaovenda as p_v
    where a.num_doente = num_doente and extract(year from a.data_registo) = extract(year from current_date) and
    extract(month from a.data_registo) = extract(month from current_date) and v_f.num_venda = p_v.num_venda
    ); 