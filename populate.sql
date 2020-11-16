insert into regiao values(1, 'Norte', 3689000);
insert into regiao values(2, 'Centro', 2327000);
insert into regiao values(3, 'Lisboa', 2884000);
insert into regiao values(4, 'Alentejo', 760099);
insert into regiao values(5, 'Algarve', 451006);

insert into concelho values(1, 1, 'Arouca', 22359);
insert into concelho values(2, 2, 'Aveiro', 55000);
insert into concelho values(3, 3, 'Barreiro', 78764);
insert into concelho values(4, 1, 'Braga', 189331);
insert into concelho values(5, 1, 'Bragança', 35341);
insert into concelho values(6, 2, 'Coimbra', 105842);
insert into concelho values(7, 4, 'Évora', 56596);

insert into instituicao values('Farmácia 1', 'farmacia', 1, 1);
insert into instituicao values('Lab 1', 'laboratorio', 2, 2);
insert into instituicao values('Clínica 1', 'clinica', 3, 3);
insert into instituicao values('Hospital 1', 'hospital', 4, 7);

insert into medico values(1, 'Sancha Barroso', 'fisioterapia');
insert into medico values(2, 'Leonor Veloso', 'oftalmologia');
insert into medico values(3, 'Pedro Ramos', 'neurologia');

insert into consulta values(1, 1,("2020-08-22","15:11:18"), 'Farmácia 1');
insert into consulta values(2, 3,("2020-07-23","13:10:11"), 'Lab 1');
insert into consulta values(2, 2,("2020-09-01","12:06:05"), 'Hospital 1');

insert into prescricao value(1, 3,("2020-06-22","10:09:10"), 'paracetamol', 10);

insert into analise(1, 'oftalmologia', 2, 1, ("2019-05-31","18:00:25"), , 'Clínica 1', )









