/*insert into d_tempo (
    select default, extract(day from dia_hora), extract(dow from dia_hora), extract(week from dia_hora),
        extract(month from dia_hora), extract(quarter from dia_hora), extract(year from dia_hora) 
        from PrescricaoVenda 
    union 
    select default,extract(day from dia_hora), extract(dow from dia_hora), extract(week from dia_hora),
        extract(month from dia_hora), extract(quarter from dia_hora), extract(year from dia_hora) 
        from Analise
);  */


insert into d_instituicao (
	select distinct id_inst, nome, num_regiao, num_concelho from Instituicao
);

insert into dbo.KeyMappingTable (shipto, salpha, ssalpha)
select distinct shipto, salpha, ssalpha
from dbo.Source
where not exists (
    select *
    from dbo.KeyMappingTable
    where shipto = dbo.Source.shipto and salpha = dbo.Source.salpha and ssalpha = dbo.Source.ssalpha
 )

insert into f_presc_venda(
    select num_venda, num_cedula, num_doente,id_tempo,id_inst,substancia, quant from d_instituicao, PrescricaoVenda as pv 
    inner join VendaFarmacia as vf on pv.num_venda = vf.num_venda
    inner join d_tempo as dt on
    (extract(day from pv.dia_hora) = dt.dia and
    extract(month from pv.dia_hora) = dt.mes and
    extract(year from pv.dia_hora) = dt.ano)
);

insert into f_analise(
    select num_analise,num_cedula,num_doente,id_tempo,id_inst, nome, quant from Analise as a, d_instituicao
    inner join d_tempo as dt on
    (extract(day from a.dia_hora) = dt.dia and
    extract(month from a.dia_hora) = dt.mes and
    extract(year from a.dia_hora) = dt.ano)
);
