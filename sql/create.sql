CREATE TYPE recency_segment AS ENUM ('0-30', '31-60', '61-90', '91-120', '121-180', '181+');
CREATE TYPE frequency_segment AS ENUM ('0-4', '5-13', '14-37', '38+');

create table if not exists voucher_segments(
	country_code varchar,
	voucher_amount integer,
	"recency_segment" recency_segment unique,
	"frequency_segment" frequency_segment unique
    constraint segment check (("recency_segment" is not null and "frequency_segment" is null) 
        or ("recency_segment" is null and "frequency_segment" is not null)),
	constraint unq_segment UNIQUE(recency_segment,frequency_segment)
);

insert into voucher_segments 
values 
	('Peru', 0, '0-30', null),
	('Peru', 0, '31-60', null),
	('Peru', 0, '61-90', null),
	('Peru', 0, '91-120', null),
	('Peru', 0, '121-180', null),
	('Peru', 0, '181+', null),
	('Peru', 0, null, '0-4'),
	('Peru', 0, null, '5-13'),
	('Peru', 0, null, '14-37'),
	('Peru', 0, null, '38+')
ON CONFLICT (recency_segment, frequency_segment) DO NOTHING;