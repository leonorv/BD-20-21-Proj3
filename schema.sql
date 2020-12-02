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
    constraint RI_consulta_2 unique(num_doente, dia_hora, nome_instituicao)
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
    num_venda integer primary key, 
    inst char(50) not null,
    data_registo timestamp not null,
    substancia char(50) not null,
    quant integer not null check(quant > 0),
    preco decimal(6,2) not null check(preco > 0), 
    foreign key(inst) references Instituicao(nome) on delete cascade on update cascade
);

create table PrescricaoVenda(
    num_cedula integer not null,
    num_doente integer not null,
    dia_hora timestamp not null,
    substancia char(50) not null,
    num_venda integer not null unique,
    foreign key(num_venda) references VendaFarmacia(num_venda) on delete cascade on update cascade,
    foreign key(num_cedula, num_doente, dia_hora, substancia) references Prescricao(num_cedula, num_doente, dia_hora, substancia) on delete cascade on update cascade, 
    primary key(num_cedula, num_doente, dia_hora, substancia, num_venda) 
);


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
    primary key(num_analise)
);
