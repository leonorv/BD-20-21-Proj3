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

create table regiao(
    num_regiao serial not null unique,
    nome char(50) not null unique,
    num_habitantes integer not null unique,
    primary key(num_regiao);
);

create table concelho(
    num_concelho serial not null unique,
    num_regiao serial not null unique,
    nome char(50) not null unique,
    num_habitantes integer not null unique,
    foreign key(num_regiao) references regiao(num_regiao) ON DELETE CASCADE,
    primary key(num_concelho, num_regiao);
);

create table instituicao(
    nome char(50) not null unique,
    
);


