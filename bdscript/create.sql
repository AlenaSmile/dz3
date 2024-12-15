create table if not exists public.teachers (
	id_teacher serial primary key not null,
	fio varchar(500) not null,
	phone char(10) null,
	email varchar null,
	comnt text null
);

create table if not exists public.variants (
	id_variant serial primary key not null,
	title varchar(200) not null,
	vcreated timestamp default now(),
	teacher_id int not null references teachers(id_teacher)
);

create table if not exists public.tests (
	id_test serial primary key not null,
	tname varchar(200) null,
	tcontent text not null,
	teacher_id int null references teachers(id_teacher)
);

create table if not exists public.variants_tests (
	variant_id int not null references variants(id_variant),
	test_id int not null references tests(id_test),
	tnumber int null,
	unique(variant_id, test_id)
);
