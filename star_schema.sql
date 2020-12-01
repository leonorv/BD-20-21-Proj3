drop table if exists d_tempo cascade;
drop table if exists d_instituicao cascade;
drop table if exists f_presc_venda cascade;
drop table if exists f_analise cascade;

create table d_tempo(
    id_tempo serial not null,
    dia integer not null,
    dia_da_semana integer not null,
    semana integer not null,
    mes integer not null,
    trimestre integer not null,
    ano integer not null,
    primary key(id_tempo)
);

create table d_instituicao(
    id_inst serial not null,
    nome char(50) not null,
    num_regiao integer not null,
    num_concelho integer not null,
    foreign key(nome) references Instituicao(nome) on delete cascade on update cascade,
    foreign key(num_regiao) references Regiao(num_regiao) on delete cascade on update cascade,
    foreign key(num_concelho) references Concelho(num_concelho) on delete cascade on update cascade,
    primary key(id_inst)
);

create table f_presc_venda(
    id_presc_venda integer not null unique,
    id_medico integer not null,
    num_doente integer not null,
    id_data_registo integer not null,
    id_inst integer not null,
    substancia char(50) not null,
    quant integer not null,
    foreign key(id_presc_venda) references PrescricaoVenda(num_venda) on delete cascade on update cascade,
    foreign key(id_medico) references Medico(num_cedula) on delete cascade on update cascade,
    foreign key(id_data_registo) references d_tempo(id_tempo) on delete cascade on update cascade,
    foreign key(id_inst) references d_instituicao(id_inst) on delete cascade on update cascade,
    primary key(id_data_registo, id_inst)
);

create table f_analise(
    id_analise integer not null unique,
    id_medico integer not null,
    num_doente integer not null,
    id_data_registo integer not null,
    id_inst integer not null,
    nome char(50) not null,
    quant integer not null,
    foreign key(id_analise) references Analise(num_analise) on delete cascade on update cascade,
    foreign key(id_medico) references Medico(num_cedula) on delete cascade on update cascade,
    foreign key(id_data_registo) references d_tempo(id_tempo) on delete cascade on update cascade,
    foreign key(id_inst) references d_instituicao(id_inst) on delete cascade on update cascade,
    primary key(id_data_registo, id_inst)
);

