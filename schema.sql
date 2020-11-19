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

create table Regiao(
    num_regiao integer not null,
    nome char(50) not null unique check(nome in ('Norte', 'Centro', 'Lisboa', 'Alentejo', 'Algarve')),
    num_habitantes integer not null check(num_habitantes > 0),
    primary key(num_regiao)
);

create table Concelho(
    num_concelho integer not null,
    num_regiao integer not null,
    nome char(50) not null unique,
    num_habitantes integer not null check(num_habitantes > 0),
    foreign key(num_regiao) references Regiao(num_regiao) ON DELETE CASCADE ON UPDATE CASCADE,
    primary key(num_concelho, num_regiao)
);

create table Instituicao(
    nome char(50) not null,
    tipo char(20) not null check(tipo in ('farmacia', 'laboratorio', 'clinica', 'hospital')),
    num_concelho integer not null,
    num_regiao integer not null,
    foreign key(num_concelho, num_regiao) references Concelho(num_concelho, num_regiao) ON DELETE CASCADE ON UPDATE CASCADE,
    primary key(nome)
);

create table Medico(
    num_cedula integer not null unique,
    nome char(50) not null, 
    especialidade char(50) not null,
    primary key(num_cedula)
);

create table Consulta(
    num_cedula integer not null,
    num_doente integer not null,
    dia_hora timestamp not null check(extract(dow from dia_hora) not in (1, 7)),
    nome_instituicao char(50) not null,
    foreign key(num_cedula) references Medico(num_cedula) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key(nome_instituicao) references Instituicao(nome) ON DELETE CASCADE ON UPDATE CASCADE,
    primary key(num_cedula, num_doente, dia_hora),
    constraint RI_consulta_2 unique(num_doente, dia_hora, nome_instituicao)
);

create table Prescricao(
    num_cedula integer not null,
    num_doente integer not null,
    dia_hora timestamp not null,
    substancia char(50) not null,
    quant integer not null check(quant > 0),
    foreign key(num_cedula, num_doente, dia_hora) references Consulta(num_cedula, num_doente, dia_hora) ON DELETE CASCADE ON UPDATE CASCADE,
    primary key(num_cedula, num_doente, dia_hora, substancia)
);



create table VendaFarmacia(
    num_venda integer not null, 
    inst char(50) not null,
    data_registo timestamp not null, 
    substancia char(50) not null,
    quant integer not null,
    preco decimal(6,2) not null, 
    foreign key(inst) references Instituicao(nome) ON DELETE CASCADE ON UPDATE CASCADE,
    primary key(num_venda)
);

create table PrescricaoVenda(
    num_cedula integer not null,
    num_doente integer not null,
    dia_hora timestamp not null,
    substancia char(50) not null,
    num_venda integer not null,
    foreign key(num_venda) references VendaFarmacia(num_venda) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key(num_cedula, num_doente, dia_hora, substancia) references Prescricao(num_cedula, num_doente, dia_hora, substancia) ON DELETE CASCADE ON UPDATE CASCADE, 
    primary key(num_cedula, num_doente, dia_hora, substancia, num_venda) 
);

create function analise.getEspecialidade(
    num_cedula integer
)
returns char(50)
begin
    return query
    select m.especialidade from Medico as m where m.num_cedula = num_cedula;
end;
/*
CREATE FUNCTION sales.udfNetSale(
    @quantity INT,
    @list_price DEC(10,2),
    @discount DEC(4,2)
)
RETURNS DEC(10,2)
AS 
BEGIN
    RETURN @quantity * @list_price * (1 - @discount);
END;*/

create table Analise(
    num_analise integer not null,
    especialidade char(50) not null, 
    num_cedula integer, 
    num_doente integer, 
    dia_hora timestamp, 
    data_registo timestamp not null, 
    nome char(50) not null, 
    quant integer not null, 
    inst char(50) not null,
    foreign key(num_cedula, num_doente, dia_hora) references Consulta(num_cedula, num_doente, dia_hora),
    foreign key(inst) references Instituicao(nome) ON DELETE CASCADE ON UPDATE CASCADE,
    primary key(num_analise),
    constraint RI_analise check((num_cedula = null and num_doente = null and dia_hora = null) or 
    getEspecialidade(num_cedula) = especialidade)
);


