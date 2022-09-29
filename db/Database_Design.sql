-- public.tbl_product definition

-- Drop table

-- DROP TABLE public.tbl_product;

CREATE TABLE public.tbl_product (
	pr_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	pr_name varchar(150) NULL,
	pr_url varchar(200) NULL,
	pr_store int4 NULL,
	pr_price float NULL,
	CONSTRAINT tbl_product_pkey PRIMARY KEY (pr_id)
);

-- public.tbl_store definition

-- Drop table

-- DROP TABLE public.tbl_store;

CREATE TABLE public.tbl_store (
	store_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	store_name varchar(30) NULL,
	CONSTRAINT tbl_store_pkey PRIMARY KEY (store_id)
);


-- public.tbl_product foreign keys

ALTER TABLE public.tbl_product ADD CONSTRAINT fk_store FOREIGN KEY (pr_store) REFERENCES public.tbl_store(store_id);

-- public.tbl_product_images definition

-- Drop table

-- DROP TABLE public.tbl_product_images;

CREATE TABLE public.tbl_product_images (
	img_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	pr_id int4 NULL,
	img_url varchar(150) NULL,
	img_path varchar(150) NULL,
	CONSTRAINT tbl_product_images_pkey PRIMARY KEY (img_id)
);


-- public.tbl_product_images foreign keys

ALTER TABLE public.tbl_product_images ADD CONSTRAINT fk_imgs FOREIGN KEY (pr_id) REFERENCES public.tbl_product(pr_id);

