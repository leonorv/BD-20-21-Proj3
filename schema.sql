/*timestamp format: 2018-9-20 23:59:59*/
drop table regiao cascade;
drop table concelho cascade;
drop table instituicao cascade;
drop table medico cascade;
drop table consulta cascade;
drop table prescricao cascade;
drop table analise cascade;
drop table venda_farmacia cascade;
drop table instituicao cascade;
drop table prescricao_venda cascade;

create table regiao (
    num_regiao serial not null,
    nome char(50) not null unique check(nome in ('Norte', 'Centro', 'Lisboa', 'Alentejo', 'Algarve')),
    num_habitantes integer not null check(num_habitantes > 0),
    primary key(num_regiao)
);

create table concelho (
    num_concelho serial not null,
    num_regiao serial not null,
    nome char(50) not null unique,
    num_habitantes integer not null check(num_habitantes > 0),
    foreign key(num_regiao) references regiao(num_regiao) on delete cascade,
    primary key(num_concelho, num_regiao)
);

create table instituicao (
    nome char(50) not null unique,
    tipo char(20) not null check(tipo in ('farmacia', 'laboratorio', 'clinica', 'hospital')),
    num_concelho serial not null,
    num_regiao serial not null,
    foreign key(num_concelho, num_regiao) references concelho(num_concelho, num_regiao) on delete cascade,
    primary key(nome)
);

create table medico (
    num_cedula serial not null,
    nome char(50) not null, 
    especialidade char(50) not null,
    primary key(num_cedula)
);

create table consulta (
    num_cedula serial not null,
    num_doente serial not null,
    dia_hora timestamp not null check(weekday(cast(dia_hora as date)) not in (5, 6)),
    nome_instituicao char(50) not null,
    foreign key(num_cedula) references medico(num_cedula) on delete cascade,
    foreign key(nome_instituicao) references instituicao(nome) on delete cascade,
    primary key(num_cedula, num_doente, dia_hora),
    constraint RI_consulta_2 unique(num_doente, dia_hora, nome_instituicao)
);

create table prescricao (
    num_cedula serial not null,
    num_doente serial not null,
    dia_hora timestamp not null,
    substancia​ char(50) not null,
    quant integer not null check(quant > 0),
    foreign key(num_cedula, num_doente, dia_hora) references consulta(num_cedula, num_doente, dia_hora) on delete cascade,
    primary key(num_cedula, num_doente, dia_hora, substancia​)
);

create table analise (​
    ​num_analise​ serial not null,
    especialidade char(50) not null, 
    num_cedula serial not null, 
    num_doente serial not null, 
    dia_hora timestamp, 
    data_registo timestamp not null, 
    nome char(50) not null, 
    quant integer not null, 
    inst char(50) not null,
    foreign key(num_cedula, num_doente, dia_hora) references consulta(num_cedula, num_doente, dia_hora) on delete cascade,
    foreign key(inst) references instituicao(nome) on delete cascade,
    primary key(num_analise),
    constraint RI_analise check((num_cedula null and num_doente null and dia_hora null) or check(consulta.especialidade == especialidade))
);

create table venda_farmacia (
    num_venda serial not null, 
    inst char(50) not null unique,
    data_registo timestamp not null, 
    substancia char(50) not null,
    quant integer not null,
    preco decimal(6,2) not null, 
    foreign key(inst) references instituicao(nome) on delete cascade,
    primary key(num_venda)
);

create table prescricao_venda (
    num_cedula serial not null,
    num_doente serial not null,
    dia_hora timestamp not null,
    substancia char(50) not null,
    num_venda serial not null,
    foreign key(num_venda) references venda_farmacia(num_venda),
    foreign key(num_cedula, num_doente, dia_hora, substancia) references prescricao(num_cedula, num_doente, dia_hora, substancia),
    primary key(num_cedula, num_doente, dia_hora, substancia, num_venda) 
);