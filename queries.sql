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
select distinct i.nome, m.nome
    from vendafarmacia as v_f, prescricaovenda as p_v, instituicao as i, concelho as c, medico as m
    where m.num_cedula = p_v.num_cedula and v_f.substancia = 'aspirina' and c.nome = 'Arouca' and i.tipo = farmacia
    and c.num_concelho = i.num_concelho and v_f.num_venda = p_v.num_venda and i.nome = v_f.inst
    and extract(year from current_date) = extract(year from v_f.data_registo) 
    );
    
select m.nome
from medico as m, instituicao as i
where not exists (
    select i.nome
    from instituicao as i, concelho as c
    where i.tipo = 'farmacia' and c.nome = 'Arouca' and i.num_concelho = c.num_concelho
    except
    select i.nome
    from vendafarmacia as v_f, prescricaovenda as p_v, instituicao as i, concelho as c, medico as m
    where m.num_cedula = p_v.num_cedula and v_f.substancia = 'aspirina' and c.nome = 'Arouca' 
    and c.num_concelho = i.num_concelho and v_f.num_venda = p_v.num_venda and i.nome = v_f.inst
    and extract(year from current_date) = extract(year from v_f.data_registo)
    );


/*QUERY 4*/
select distinct a.num_doente 
from analise as a
where extract(year from a.data_registo) = extract(year from current_date) and
extract(month from a.data_registo) = extract(month from current_date)
and not exists (
    select * from venda_farmacia as v_f, prescricaovenda as p_v
    where a.num_doente = num_doente and where extract(year from a.data_registo) = extract(year from current_date) and
    extract(month from a.data_registo) = extract(month from current_date and v_f.num_venda = p_v.num_venda
    );



    