insert into d_tempo (dia, dia_da_semana, semana, mes, trimestre, ano) (
    select extract(day from data_registo), extract(dow from data_registo), extract(week from data_registo),
        extract(month from data_registo), extract(quarter from data_registo), extract(year from data_registo) 
        from PrescricaoVenda as pv inner join VendaFarmacia as vf on pv.num_venda = vf.num_venda
    union 
    select extract(day from a.data_registo), extract(dow from a.data_registo), extract(week from a.data_registo),
        extract(month from a.data_registo), extract(quarter from a.data_registo), extract(year from a.data_registo) 
        from Analise as a
);  

insert into d_instituicao(nome,num_regiao,num_concelho) (
	select nome, num_regiao, num_concelho from Instituicao
);

insert into f_presc_venda (
    select pv.num_venda, num_cedula, num_doente, id_tempo, id_inst, pv.substancia, quant from d_instituicao
    inner join VendaFarmacia as vf on vf.inst = d_instituicao.nome
    inner join PrescricaoVenda as pv on pv.num_venda = vf.num_venda
    inner join d_tempo as dt on
    (extract(day from vf.data_registo) = dt.dia and
    extract(month from vf.data_registo) = dt.mes and
    extract(year from vf.data_registo) = dt.ano)
    order by pv.num_venda
);

insert into f_analise (
    select num_analise,num_cedula,num_doente,id_tempo,id_inst, a.nome, quant from Analise as a
    inner join d_instituicao as di on a.inst = di.nome
    inner join d_tempo as dt on
    (extract(day from a.data_registo) = dt.dia and
    extract(month from a.data_registo) = dt.mes and
    extract(year from a.data_registo) = dt.ano)
    order by num_analise
);
