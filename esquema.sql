drop table if exists entradas;
create table entradas (
  id integer primary key autoincrement,
  nome string not null,
  email string not null,
  telefone string not null,
  salmensal float not null,
  media float null,
  receita float null,
  bonus float null
);
