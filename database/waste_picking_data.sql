create TABLE operating_area (
Area_id primary key,
municipality_id integer references municipalities(id),
sorting_location varchar(40) not null,
waste_picker_SAWPRS_id integer references waste_pickers(SAWPRS_id),
truck_drivers_id integer references truck_drivers(id),
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp
);

create TABLE truck_drivers (
truck_drivers_id primary key,
company_name varchar(40) not null,
vehicle_id integer references vehicles(id),
truck_number_plate varchar(12),
weight_kg REAL,
volume_cm3 REAL,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp
);

create TABLE user_auth (
    user_id serial primary key,
    name varchar(50) unique not null,
    surname varchar(50) not null,
    email_address varchar(20) not null,
    waste_pickers_SAWPRS_id integer references waste_pickers(SAWPRS_id),
    truck_drivers_id integer references truck_drivers(id),
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp
);

create TABLE waste_pickers (
    SAWPRS_id serial primary key,
    registration_status boolean not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp
);



INSERT INTO user_auth (
  user_id, name, surname, email_address, waste_pickers_SAWPRS_id, truck_drivers_id, created_at, updated_at
) VALUES
  (1, 'Nomsa', 'Nkosi', 'nomsa.nkosi@eco.org', 2001, 3001, '2025-10-22 09:05:15', '2025-10-22 09:05:15'),
  (2, 'Siyabonga', 'Mthembu', 'siya.mth@green.co.za', 2003, 3002, '2025-10-22 09:25:08', '2025-10-22 09:25:08'),
  (3, 'Lerato', 'Dlamini', 'lerato.d@eco.org', 2004, 3003, '2025-10-22 09:42:50', '2025-10-22 09:42:50'),
  (4, 'Themba', 'Khumalo', 'themba.kh@haul.co.za', 2006, 3004, '2025-10-22 10:01:42', '2025-10-22 10:01:42'),
  (5, 'Phindi', 'Mabaso', 'phindi.m@waste.co.za', 2008, 3005, '2025-10-22 10:21:53', '2025-10-22 10:21:53'),
  (6, 'Thabo', 'Radebe', 'thabo.r@clean.org', 2009, 3006, '2025-10-22 10:44:32', '2025-10-22 10:44:32'),
  (7, 'Ayanda', 'Sithole', 'ayanda.s@recyc.co.za', 2012, 3007, '2025-10-22 11:09:27', '2025-10-22 11:09:27'),
  (8, 'Precious', 'Mokoena', 'prec.m@haul.co.za', 2013, 3008, '2025-10-22 11:31:10', '2025-10-22 11:31:10'),
  (9, 'Kabelo', 'Ngobeni', 'kab.ng@eco.org', 2015, 3009, '2025-10-22 11:50:38', '2025-10-22 11:50:38'),
  (10, 'Zanele', 'Mashaba', 'zan.mash@green.co.za', 2018, 3010, '2025-10-22 12:05:59', '2025-10-22 12:05:59');
SELECT * FROM user_auth;

INSERT INTO truck_drivers (
  truck_drivers_id, company_name, vehicle_id, truck_number_plate, weight_kg, volume_cm3, created_at, updated_at
) VALUES
  (3001, 'EcoHaul Logistics', 1001, 'NDY458GP', 8.50, 12.70, '2025-10-22 08:30:10', '2025-10-22 08:30:10'),
  (3002, 'GreenPath Transport', 1002, 'JBL329EC', 9.25, 15.40, '2025-10-22 08:40:55', '2025-10-22 08:40:55'),
  (3003, 'Recyclo Movers', 1003, 'CFM872NW', 7.80, 10.90, '2025-10-22 09:10:13', '2025-10-22 09:10:13'),
  (3004, 'WastePro Trucking', 1004, 'TVL632GP', 12.10, 18.50, '2025-10-22 09:25:20', '2025-10-22 09:25:20'),
  (3005, 'CleanCity Haulage', 1005, 'FZK908WC', 10.35, 14.60, '2025-10-22 09:55:41', '2025-10-22 09:55:41'),
  (3006, 'EnviroFleet SA', 1006, 'BHK121MP', 9.90, 13.85, '2025-10-22 10:02:38', '2025-10-22 10:02:38');

SELECT * FROM truck_drivers;



INSERT INTO operating_area (
  Area_id, municipality_id, sorting_location, waste_picker_SAWPRS_id, truck_drivers_id, created_at, updated_at
) VALUES
  (1, 10, 'Mamelodi East Sorting Hub', 2001, 3001, '2025-10-20 08:32:15', '2025-10-20 08:32:15'),
  (2, 11, 'Atteridgeville Recycling Site', 2005, 3003, '2025-10-20 09:15:22', '2025-10-20 09:15:22'),
  (3, 12, 'Centurion Industrial Park', 2007, 3007, '2025-10-20 10:12:03', '2025-10-20 10:12:03'),
  (4, 10, 'Pretoria West Sorting Facility', 2009, 3008, '2025-10-20 11:45:09', '2025-10-20 11:45:09'),
  (5, 13, 'Soshanguve Central Yard', 2012, 3011, '2025-10-20 12:03:45', '2025-10-20 12:03:45'),
  (6, 14, 'Hammanskraal Waste Depot', 2015, 3013, '2025-10-20 12:42:30', '2025-10-20 12:42:30'),
  (7, 11, 'Olievenhoutbosch Drop-off Zone', 2019, 3018, '2025-10-20 13:22:09', '2025-10-20 13:22:09'),
  (8, 15, 'Tembisa Extension 2 Yard', 2020, 3021, '2025-10-20 13:55:44', '2025-10-20 13:55:44'),
  (9, 13, 'Ga-Rankuwa Sorting Center', 2024, 3025, '2025-10-20 14:24:17', '2025-10-20 14:24:17'),
  (10, 16, 'Silverton Recycling Site', 2028, 3030, '2025-10-20 15:01:33', '2025-10-20 15:01:33');

SELECT * FROM operating_area;

INSERT INTO waste_pickers (
    SAWPRS_id, registration_status, created_at, updated_at
) VALUES
    (2001, true,  '2025-10-01 08:12:03', '2025-10-15 14:33:45'),
    (2002, false, '2025-09-28 11:45:09', '2025-10-05 09:18:27'),
    (2003, true,  '2025-10-02 10:20:19', '2025-10-18 13:01:55'),
    (2004, true,  '2025-09-26 12:14:22', '2025-10-19 09:42:07'),
    (2005, false, '2025-09-30 07:53:52', '2025-10-10 15:28:21'),
    (2006, true,  '2025-10-03 09:31:40', '2025-10-17 16:20:30'),
    (2007, false, '2025-09-25 08:07:53', '2025-10-09 13:09:46'),
    (2008, true,  '2025-10-04 10:02:14', '2025-10-20 18:55:42'),
    (2009, true,  '2025-09-29 06:48:35', '2025-10-16 08:14:59'),
    (2010, false, '2025-09-27 09:05:55', '2025-10-11 11:38:19'),
    (2011, true,  '2025-09-30 13:14:45', '2025-10-23 09:52:27'),
    (2012, true,  '2025-10-01 09:12:00', '2025-10-21 16:17:03'),
    (2013, false, '2025-09-24 08:31:51', '2025-10-10 10:20:21'),
    (2014, true,  '2025-10-05 11:04:44', '2025-10-22 12:38:59'),
    (2015, true,  '2025-09-28 09:42:31', '2025-10-19 11:47:11'),
    (2016, false, '2025-09-30 10:22:43', '2025-10-16 13:40:33'),
    (2017, true,  '2025-10-03 12:16:57', '2025-10-20 14:22:40'),
    (2018, true,  '2025-10-02 07:55:09', '2025-10-22 15:09:13'),
    (2019, false, '2025-09-27 10:07:26', '2025-10-13 09:59:28'),
    (2020, true,  '2025-09-29 11:22:45', '2025-10-24 10:19:15');
SELECT * FROM waste_pickers;

