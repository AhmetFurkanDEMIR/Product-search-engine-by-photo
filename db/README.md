![](https://img.shields.io/badge/Oracle-F80000?style=for-the-badge&logo=oracle&logoColor=black) ![](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) 


# Database design


**Relational table design**

![SQL_Schema](https://user-images.githubusercontent.com/54184905/194742053-e4d0c65b-697c-4c8d-b022-e269deb31c49.png)


**SQL codes of tables**

```sql
-- Design codes of tables (Ahmet Furkan Demir)

-- public.tbl_category definition

-- Drop table

-- DROP TABLE public.tbl_category;

CREATE TABLE public.tbl_category (
	cat_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	cat_name varchar(30) NULL,
	CONSTRAINT tbl_category_pkey PRIMARY KEY (cat_id)
);


-- public.tbl_product definition

-- Drop table

-- DROP TABLE public.tbl_product;

CREATE TABLE public.tbl_product (
	pr_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	pr_name varchar(150) NULL,
	pr_url varchar(200) NULL,
	pr_category int4 NULL,
	pr_store int4 NULL,
	CONSTRAINT tbl_product_pkey PRIMARY KEY (pr_id)
);


-- public.tbl_product foreign keys

ALTER TABLE public.tbl_product ADD CONSTRAINT fk_category FOREIGN KEY (pr_category) REFERENCES public.tbl_category(cat_id);
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


-- public.tbl_store definition

-- Drop table

-- DROP TABLE public.tbl_store;

CREATE TABLE public.tbl_store (
	store_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	store_name varchar(30) NULL,
	CONSTRAINT tbl_store_pkey PRIMARY KEY (store_id)
);
```


**Backup database (Oracle)**

```console
Host: postgresql.ahmetfurkandemir.com
Port: 5432
Database: postgres
Username: postgres
Password: 5,8f4ds8/*-%&gfd85f6ds*-dd

(Machine connection)
sudo ssh -i ssh-key-2022-09-20.key ubuntu@141.147.10.228
```
