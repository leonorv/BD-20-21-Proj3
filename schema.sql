/*timestamp format: 2017-9-20 23:59:59*/
drop table if exists Regiao cascade;
drop table if exists Concelho cascade;
drop table if exists Instituicao cascade;
drop table if exists Medico cascade;
drop table if exists Consulta cascade;
drop table if exists Prescricao cascade;
drop table if exists VendaFarmacia cascade;
drop table if exists PrescricaoVenda cascade;
drop table if exists Analise cascade;
drop function if exists getEspecialidade(integer) cascade;
drop function if exists getNConsultas(timestamp, char(50), integer);

create table Regiao(
    num_regiao integer not null unique,
    nome char(50) not null unique check(nome in ('Norte', 'Centro', 'Lisboa', 'Alentejo', 'Algarve')),
    num_habitantes integer not null check(num_habitantes > 0),
    primary key(num_regiao)
);

create table Concelho(
    num_concelho integer not null unique,
    num_regiao integer not null,
    nome char(50) not null,
    num_habitantes integer not null check(num_habitantes > 0),
    foreign key(num_regiao) references Regiao(num_regiao) on delete cascade on update cascade,
    primary key(num_concelho, num_regiao)
);

create table Instituicao(
    nome char(50) not null unique,
    tipo char(20) not null check(tipo in ('farmacia', 'laboratorio', 'clinica', 'hospital')),
    num_concelho integer not null,
    num_regiao integer not null,
    foreign key(num_concelho, num_regiao) references Concelho(num_concelho, num_regiao) on delete cascade on update cascade,
    primary key(nome)
);


/*extensão procedimental para a restrição de integridade RI-100*/
create or replace function getNConsultas (dh timestamp, ni char(50), nc integer)
returns integer as $nConsultas$
declare
	nConsultas integer;
begin
   select count(c.num_cedula) into nConsultas from Consulta as c where extract(year from c.dia_hora) = extract(year from dh) and extract(week from c.dia_hora) = extract(week from dh) and ni = c.nome_instituicao and nc = c.num_cedula;
   return nConsultas;
end;
$nConsultas$ language plpgsql;

create table Medico(
    num_cedula integer not null unique,
    nome char(50) not null, 
    especialidade char(50) not null,
    primary key(num_cedula)
);

create table Consulta(
    num_cedula integer not null,
    num_doente integer not null,
    dia_hora timestamp not null check(extract(dow from dia_hora) not in (0, 6)),
    nome_instituicao char(50) not null,
    foreign key(num_cedula) references Medico(num_cedula) on delete cascade on update cascade,
    foreign key(nome_instituicao) references Instituicao(nome) on delete cascade on update cascade,
    primary key(num_cedula, num_doente, dia_hora),
    constraint RI_consulta_2 unique(num_doente, dia_hora, nome_instituicao),
    constraint RI_100 check(getNConsultas(dia_hora, nome_instituicao, num_cedula) < 1)
);

create table Prescricao(
    num_cedula integer not null,
    num_doente integer not null,
    dia_hora timestamp not null,
    substancia char(50) not null,
    quant integer not null check(quant > 0),
    foreign key(num_cedula, num_doente, dia_hora) references Consulta(num_cedula, num_doente, dia_hora) on delete cascade on update cascade,
    primary key(num_cedula, num_doente, dia_hora, substancia)
);



create table VendaFarmacia(
    num_venda integer not null unique, 
    inst char(50) not null,
    data_registo timestamp not null,
    substancia char(50) not null,
    quant integer not null check(quant > 0),
    preco decimal(6,2) not null check(preco > 0), 
    foreign key(inst) references Instituicao(nome) on delete cascade on update cascade,
    primary key(num_venda)
);

create table PrescricaoVenda(
    num_cedula integer not null,
    num_doente integer not null,
    dia_hora timestamp not null,
    substancia char(50) not null,
    num_venda integer not null,
    foreign key(num_venda) references VendaFarmacia(num_venda) on delete cascade on update cascade,
    foreign key(num_cedula, num_doente, dia_hora, substancia) references Prescricao(num_cedula, num_doente, dia_hora, substancia) on delete cascade on update cascade, 
    primary key(num_cedula, num_doente, dia_hora, substancia, num_venda) 
);


/*extensão procedimental para a restrição de integridade da analise*/
create or replace function getEspecialidade (nc integer)
returns char(50) as $especialidade$
declare
	especialidade char(50);
begin
   select m.especialidade into especialidade from Medico as m where m.num_cedula = nc;
   return especialidade;
end;
$especialidade$ language plpgsql;

create table Analise(
    num_analise integer not null,
    especialidade char(50) not null, 
    num_cedula integer, 
    num_doente integer, 
    dia_hora timestamp, 
    data_registo timestamp not null, 
    nome char(50) not null, 
    quant integer not null check(quant > 0), 
    inst char(50) not null,
    foreign key(num_cedula, num_doente, dia_hora) references Consulta(num_cedula, num_doente, dia_hora),
    foreign key(inst) references Instituicao(nome) on delete cascade on update cascade,
    primary key(num_analise),
    constraint RI_analise check((num_cedula is null and num_doente is null and dia_hora is null) or getEspecialidade(num_cedula) = especialidade)
);
