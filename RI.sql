drop function if exists verifica_especialidade();
drop function if exists verifica_consultas(); 
drop trigger if exists verifica_consultas_trigger on Consulta;
drop trigger if exists verifica_especialidade_trigger on Analise;

/*RI-100: ​ um médico não pode dar mais de 100 consultas por semana na mesma instituição*/
/*extensão procedimental para a restrição de integridade RI-100*/
create or replace function verifica_consultas ()
returns trigger as $$
declare
	nConsultas integer;
begin
   select count(c.num_cedula) into nConsultas from Consulta as c where extract(year from c.dia_hora) = extract(year from new.dia_hora) and extract(week from c.dia_hora) = extract(week from new.dia_hora) and new.nome_instituicao = c.nome_instituicao and new.num_cedula = c.num_cedula;
   if (nConsultas >= 100) then
      raise exception 'O médico % não pode dar mais do que 100 consultas por semana.', new.num_cedula;
   end if;
   return new;
end;
$$ language plpgsql;

create trigger verifica_consultas_trigger before insert or update on Consulta
for each row execute procedure verifica_consultas();

/*RI-análise: ​ numa análise, a consulta associada pode estar omissa; não estando, a especialidade 
da consulta tem de ser igual à do médico*/
/*extensão procedimental para a restrição de integridade da analise*/
create or replace function verifica_especialidade ()
returns trigger as $$
declare
	especialidade char(50);
begin
   select m.especialidade into especialidade from Medico as m where m.num_cedula = new.num_cedula;
   if (new.num_cedula is not null and new.num_doente is not null and new.dia_hora is not null and especialidade != new.especialidade) then
      raise exception 'A especialidade da consulta associada não corresponde à especialidade %.', new.especialidade;
   end if;
   return new;
end;
$$ language plpgsql;

create trigger verifica_especialidade_trigger before insert or update on Analise
for each row execute procedure verifica_especialidade();

