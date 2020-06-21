create table if not exists voucher_raw(
	"timestamp" timestamp,
	country_code varchar,
	last_order_ts timestamp,
	first_order_ts timestamp,
	total_orders integer,
	vourcher_amount integer
);

CREATE TYPE recency_segment AS ENUM ('30-60', '60-90', '90-120', '120-180', '180+');
CREATE TYPE frequency_segment AS ENUM ('0-4', '5-13', '13-37', '38+');

create table if not exists voucher_segments(
	country_code varchar,
	vourcher_amount integer,
	"recency_segment" recency_segment,
	"frequency_segment" frequency_segment
    constraint segment check (("recency_segment" is not null and "frequency_segment" is null) 
        or ("recency_segment" is null and "frequency_segment" is not null))
);

