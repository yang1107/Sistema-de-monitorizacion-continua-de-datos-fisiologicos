CREATE SEQUENCE "public".cuenta_id_cuenta_seq START WITH 1 INCREMENT BY 1;

CREATE  TABLE "public".calorias (
	time_calorias        timestamp  NOT NULL  ,
	timestamp_calorias   bigint    ,
	id_calorias          serial  NOT NULL  ,
	nombre_dispositivo   text    ,
	model_id             text    ,
	device_id            text    ,
	calorias             double precision    ,
	nombre_usuario       text
 );

CREATE  TABLE "public".calorias_entrenamiento (
	time_calorias        timestamp  NOT NULL  ,
	id_calorias          serial    ,
	calorias             double precision    ,
	id_entrenamiento     bigint
 );

CREATE  TABLE "public".cuenta (
	id_cuenta            integer DEFAULT nextval('cuenta_id_cuenta_seq'::regclass) NOT NULL  ,
	nombre_cuenta        text    ,
	CONSTRAINT pk_cuenta PRIMARY KEY ( id_cuenta ),
	CONSTRAINT unq_cuenta_nombre_cuenta UNIQUE ( nombre_cuenta )
 );

CREATE  TABLE "public".distancia (
	time_distancia       timestamp  NOT NULL  ,
	timestamp_distancia  bigint    ,
	id_distancia         serial  NOT NULL  ,
	nombre_dispositivo   text    ,
	model_id             text    ,
	device_id            text    ,
	distancia             double precision    ,
	nombre_usuario       text
 );

CREATE  TABLE "public".distancia_entrenamiento (
	time_distancia       timestamp  NOT NULL  ,
	id_distancia         serial    ,
	distancia            double precision    ,
	id_entrenamiento     bigint
 );

CREATE  TABLE "public".elevacion (
	time_elevacion       timestamp  NOT NULL  ,
	timestamp_elevacion  bigint    ,
	id_elevacion         serial  NOT NULL  ,
	nombre_dispositivo   text    ,
	model_id             text    ,
	device_id            text    ,
	elevacion             double precision    ,
	nombre_usuario       text
 );

CREATE  TABLE "public".elevacion_entrenamiento (
	time_elevacion       timestamp  NOT NULL  ,
	id_elevacion         serial    ,
	elevacion            double precision    ,
	id_entrenamiento     bigint
 );

CREATE  TABLE "public".heart_rate (
	time_heart_rate      timestamp  NOT NULL  ,
	timestamp_heart_rate bigint    ,
	id_heart_rate        serial  NOT NULL  ,
	nombre_dispositivo   text    ,
	model_id             text    ,
	device_id            text    ,
	heart_rate           double precision    ,
	nombre_usuario       text
 );

CREATE  TABLE "public".hr_entrenamiento (
	time_hr              timestamp  NOT NULL  ,
	id_hr                serial  NOT NULL  ,
	hr_average           double precision    ,
	hr_min               double precision    ,
	hr_max               double precision    ,
	hr_zone_0            double precision    ,
	hr_zone_1            double precision    ,
	hr_zone_2            double precision    ,
	hr_zone_3            double precision    ,
	id_entrenamiento     bigint
 );

CREATE  TABLE "public".hr_suenio (
	time_hr              timestamp  NOT NULL  ,
	timestamp_hr         bigint    ,
	id_hr                serial  NOT NULL  ,
	hr_suenio            double precision    ,
	id_suenio            bigint
 );

CREATE  TABLE "public".pasos (
	time_pasos           timestamp  NOT NULL  ,
	timestamp_pasos      bigint    ,
	id_pasos             serial  NOT NULL  ,
	nombre_dispositivo   text    ,
	model_id             text    ,
	device_id            text    ,
	pasos             double precision    ,
	nombre_usuario       text
 );

CREATE  TABLE "public".pasos_entrenamiento (
	time_pasos           timestamp  NOT NULL  ,
	id_pasos             serial    ,
	pasos                double precision    ,
	id_entrenamiento     bigint
 );

CREATE  TABLE "public".senial_ecg (
	time_senial          timestamp  NOT NULL  ,
	signal_id            bigint    ,
	valor_senial         integer
 );

CREATE  TABLE "public".spo2 (
	time_spo2            timestamp  NOT NULL  ,
	timestamp_spo2       bigint    ,
	id_spo2              serial  NOT NULL  ,
	nombre_dispositivo   text    ,
	model_id             text    ,
	device_id            text    ,
	spo2             double precision    ,
	nombre_usuario       text
 );

CREATE  TABLE "public".spo2_average_entrenamiento (
	time_spo2            timestamp  NOT NULL  ,
	id_spo2              serial    ,
	spo2_average                 double precision    ,
	id_entrenamiento     bigint
 );

CREATE  TABLE "public".usuario (
	id_usuario           serial  NOT NULL  ,
	apellido             text    ,
	nombre               text    ,
	email                text    ,
	edad                 text    ,
	altura               double precision    ,
	sexo                 text    ,
	nombre_cuenta        text    ,
	CONSTRAINT pk_usuario PRIMARY KEY ( id_usuario ),
	CONSTRAINT unq_usuario_nombre UNIQUE ( nombre ) ,
	CONSTRAINT fk_usuario_cuenta FOREIGN KEY ( nombre_cuenta ) REFERENCES "public".cuenta( nombre_cuenta )
 );

CREATE  TABLE "public".dispositivo (
	id_dispositivo       serial  NOT NULL  ,
	nombre_dispositivo   text    ,
	tipo                 text    ,
	id_modelo            text    ,
	device_id            text    ,
	nombre_usuario       text    ,
	CONSTRAINT pk_dispositivo PRIMARY KEY ( id_dispositivo ),
	CONSTRAINT unq_dispositivo_device_id UNIQUE ( device_id ) ,
	CONSTRAINT unq_dispositivo_id_modelo UNIQUE ( id_modelo ) ,
	CONSTRAINT fk_dispositivo_usuario FOREIGN KEY ( nombre_usuario ) REFERENCES "public".usuario( nombre )
 );

CREATE  TABLE "public".ecg (
	time_ecg             timestamp  NOT NULL  ,
	id_ecg               serial  NOT NULL  ,
	model_id             text    ,
	signal_id            bigint    ,
	qrs                  double precision    ,
	qt                   double precision    ,
	pr                   double precision    ,
	qtc                  double precision    ,
	nombre_usuario       text    ,
	CONSTRAINT pk_ecg PRIMARY KEY ( id_ecg ),
	CONSTRAINT fk_ecg_dispositivo FOREIGN KEY ( model_id ) REFERENCES "public".dispositivo( id_modelo )   ,
	CONSTRAINT fk_ecg_usuario FOREIGN KEY ( nombre_usuario ) REFERENCES "public".usuario( nombre )
 );

CREATE  TABLE "public".entrenamiento (
	id_entrenamiento     bigint  NOT NULL  ,
	date_entrenamiento   date  NOT NULL  ,
	startdate            timestamp    ,
	enddate              timestamp    ,
	device_id            text    ,
	modelo_disp          text    ,
	nombre_usuario       text
 );

CREATE  TABLE "public".objetivo (
	id_objetivo          serial  NOT NULL  ,
	paso                 integer    ,
	suenio               integer    ,
	peso                 integer    ,
	nombre_usuario       text    ,
	CONSTRAINT pk_objetivo PRIMARY KEY ( id_objetivo ),
	CONSTRAINT fk_objetivo_usuario FOREIGN KEY ( nombre_usuario ) REFERENCES "public".usuario( nombre )
 );

CREATE  TABLE "public".salud (
	id_salud             serial  NOT NULL  ,
	date_salud           date    ,
	device_id            text    ,
	nombre_usuario       text    ,
	time_created         bigint    ,
	CONSTRAINT pk_salud PRIMARY KEY ( id_salud ),
	CONSTRAINT fk_salud_dispositivo FOREIGN KEY ( device_id ) REFERENCES "public".dispositivo( device_id )   ,
	CONSTRAINT fk_salud_usuario FOREIGN KEY ( nombre_usuario ) REFERENCES "public".usuario( nombre )
 );

CREATE  TABLE "public".suenio (
	id_suenio            bigint  NOT NULL  ,
	date_suenio          date  NOT NULL  ,
	model_id             text    ,
	device_id            text    ,
	startdate            timestamp    ,
	enddate              timestamp    ,
	nombre_usuario       text    ,
	CONSTRAINT pk_suenio PRIMARY KEY ( id_suenio ),
	CONSTRAINT fk_suenio_dispositivo FOREIGN KEY ( model_id ) REFERENCES "public".dispositivo( id_modelo )   ,
	CONSTRAINT fk_suenio_dispositivo_0 FOREIGN KEY ( device_id ) REFERENCES "public".dispositivo( device_id )   ,
	CONSTRAINT fk_suenio_usuario FOREIGN KEY ( nombre_usuario ) REFERENCES "public".usuario( nombre )
 );

CREATE  TABLE "public".vo2max (
	id_vo2max            serial  NOT NULL  ,
	vo2max               double precision    ,
	id_salud             bigint    ,
	CONSTRAINT pk_vo2max PRIMARY KEY ( id_vo2max ),
	CONSTRAINT fk_vo2max_salud FOREIGN KEY ( id_salud ) REFERENCES "public".salud( id_salud )
 );

CREATE  TABLE "public".weight (
	id_weight            serial  NOT NULL  ,
	weight               double precision    ,
	id_salud             bigint    ,
	CONSTRAINT pk_vo2max_3 PRIMARY KEY ( id_weight ),
	CONSTRAINT fk_vo2max_salud_3 FOREIGN KEY ( id_salud ) REFERENCES "public".salud( id_salud )
 );

CREATE  TABLE "public".actividad (
	id_actividad         serial  NOT NULL  ,
	date_actividad       date  NOT NULL  ,
	device_id            text    ,
	nombre_usuario       text    ,
	modified             bigint    ,
	CONSTRAINT pk_actividad PRIMARY KEY ( id_actividad ),
	CONSTRAINT fk_actividad_usuario FOREIGN KEY ( nombre_usuario ) REFERENCES "public".usuario( nombre )   ,
	CONSTRAINT fk_actividad_dispositivo FOREIGN KEY ( device_id ) REFERENCES "public".dispositivo( device_id )
 );

CREATE  TABLE "public".bone_mass (
	id_bone_mass         serial  NOT NULL  ,
	bone_mass            double precision    ,
	id_salud             bigint    ,
	CONSTRAINT pk_vo2max_5 PRIMARY KEY ( id_bone_mass ),
	CONSTRAINT fk_vo2max_salud_5 FOREIGN KEY ( id_salud ) REFERENCES "public".salud( id_salud )
 );

CREATE  TABLE "public".calorias_actividad (
	id_calorias          serial  NOT NULL  ,
	id_actividad         bigint    ,
	calorias             double precision    ,
	total_calorias       double precision    ,
	CONSTRAINT pk_calorias_actividad PRIMARY KEY ( id_calorias ),
	CONSTRAINT fk_calorias_actividad_actividad FOREIGN KEY ( id_actividad ) REFERENCES "public".actividad( id_actividad )
 );

CREATE  TABLE "public".datos_suenio (
	id_datos             serial  NOT NULL  ,
	wakeup_duration      double precision    ,
	wakeup_count         double precision    ,
	duration_to_wakeup   double precision    ,
	total_sleep_time     double precision    ,
	sleep_efficiency     double precision    ,
	sleep_latency        double precision    ,
	waso                 double precision    ,
	light_sleep_duration double precision    ,
	deep_sleep_duration  double precision    ,
	rem_sleep_duration   double precision    ,
	hr_average           double precision    ,
	hr_min               double precision    ,
	hr_max               double precision    ,
	sleep_score          double precision    ,
	id_suenio            bigint    ,
	CONSTRAINT pk_datos_suenio PRIMARY KEY ( id_datos ),
	CONSTRAINT fk_datos_suenio_suenio FOREIGN KEY ( id_suenio ) REFERENCES "public".suenio( id_suenio )
 );

CREATE  TABLE "public".distancia_actividad (
	id_distancia         serial  NOT NULL  ,
	id_actividad         bigint    ,
	distancia            double precision    ,
	CONSTRAINT pk_elevacion_actividad_1 PRIMARY KEY ( id_distancia ),
	CONSTRAINT fk_elevacion_actividad_actividad_1 FOREIGN KEY ( id_actividad ) REFERENCES "public".actividad( id_actividad )
 );

CREATE  TABLE "public".elevacion_actividad (
	id_elevacion         serial  NOT NULL  ,
	id_actividad         bigint    ,
	elevacion            double precision    ,
	CONSTRAINT pk_elevacion_actividad PRIMARY KEY ( id_elevacion ),
	CONSTRAINT fk_elevacion_actividad_actividad FOREIGN KEY ( id_actividad ) REFERENCES "public".actividad( id_actividad )
 );

CREATE  TABLE "public".fat_free_mass (
	id_fat_free_mass     serial  NOT NULL  ,
	fat_free_mass        double precision    ,
	id_salud             bigint    ,
	CONSTRAINT pk_vo2max_8 PRIMARY KEY ( id_fat_free_mass ),
	CONSTRAINT fk_vo2max_salud_8 FOREIGN KEY ( id_salud ) REFERENCES "public".salud( id_salud )
 );

CREATE  TABLE "public".fat_mass (
	id_fat_mass          serial  NOT NULL  ,
	fat_mass             double precision    ,
	id_salud             bigint    ,
	CONSTRAINT pk_vo2max_4 PRIMARY KEY ( id_fat_mass ),
	CONSTRAINT fk_vo2max_salud_4 FOREIGN KEY ( id_salud ) REFERENCES "public".salud( id_salud )
 );

CREATE  TABLE "public".fat_ratio (
	id_fat_ratio         serial  NOT NULL  ,
	fat_ratio            double precision    ,
	id_salud             bigint    ,
	CONSTRAINT pk_vo2max_2 PRIMARY KEY ( id_fat_ratio ),
	CONSTRAINT fk_vo2max_salud_2 FOREIGN KEY ( id_salud ) REFERENCES "public".salud( id_salud )
 );

CREATE  TABLE "public".heart_pulse (
	id_heart_pulse       serial  NOT NULL  ,
	heart_pulse          double precision    ,
	id_salud             bigint    ,
	CONSTRAINT pk_vo2max_0 PRIMARY KEY ( id_heart_pulse ),
	CONSTRAINT fk_vo2max_salud_0 FOREIGN KEY ( id_salud ) REFERENCES "public".salud( id_salud )
 );

CREATE  TABLE "public".hr_actividad (
	id_hr                serial  NOT NULL  ,
	id_actividad         bigint    ,
	hr_average           double precision    ,
	hr_min               double precision    ,
	hr_max               double precision    ,
	hr_zone_0            double precision    ,
	hr_zone_1            double precision    ,
	hr_zone_2            double precision    ,
	hr_zone_3            double precision    ,
	CONSTRAINT pk_hr_actividad PRIMARY KEY ( id_hr ),
	CONSTRAINT fk_hr_actividad_actividad FOREIGN KEY ( id_actividad ) REFERENCES "public".actividad( id_actividad )
 );

CREATE  TABLE "public".hydration (
	id_hydration         serial  NOT NULL  ,
	hydration            double precision    ,
	id_salud             bigint    ,
	CONSTRAINT pk_vo2max_1 PRIMARY KEY ( id_hydration ),
	CONSTRAINT fk_vo2max_salud_1 FOREIGN KEY ( id_salud ) REFERENCES "public".salud( id_salud )
 );

CREATE  TABLE "public".intensidad_actividad (
	id_intensidad        serial  NOT NULL  ,
	id_actividad         bigint    ,
	suave                double precision    ,
	moderada             double precision    ,
	intensa              double precision    ,
	activa               double precision    ,
	CONSTRAINT pk_intensidad_actividad PRIMARY KEY ( id_intensidad ),
	CONSTRAINT fk_intensidad_actividad_actividad FOREIGN KEY ( id_actividad ) REFERENCES "public".actividad( id_actividad )
 );

CREATE  TABLE "public".muscle_mass (
	id_muscle_mass       serial  NOT NULL  ,
	muscle_mass          double precision    ,
	id_salud             bigint    ,
	CONSTRAINT pk_vo2max_6 PRIMARY KEY ( id_muscle_mass ),
	CONSTRAINT fk_vo2max_salud_6 FOREIGN KEY ( id_salud ) REFERENCES "public".salud( id_salud )
 );

CREATE  TABLE "public".paso_actividad (
	id_pasos             serial  NOT NULL  ,
	id_actividad         bigint    ,
	pasos                double precision    ,
	CONSTRAINT pk_elevacion_actividad_0 PRIMARY KEY ( id_pasos ),
	CONSTRAINT fk_elevacion_actividad_actividad_0 FOREIGN KEY ( id_actividad ) REFERENCES "public".actividad( id_actividad )
 );

CREATE  TABLE "public".pulse_wave_velocity (
	id_pulse_wave_velocity serial  NOT NULL  ,
	pulse_wave_velocity  double precision    ,
	id_salud             bigint    ,
	CONSTRAINT pk_vo2max_7 PRIMARY KEY ( id_pulse_wave_velocity ),
	CONSTRAINT fk_vo2max_salud_7 FOREIGN KEY ( id_salud ) REFERENCES "public".salud( id_salud )
 );

 CREATE  TABLE "public".agua (
	id_agua              serial  NOT NULL  ,
	agua                 double precision    ,
	id_salud             bigint    ,
	CONSTRAINT pk_imc_2 PRIMARY KEY ( id_agua )
 );

CREATE  TABLE "public".imc (
	id_imc               serial  NOT NULL  ,
	imc                  double precision    ,
	id_salud             bigint    ,
	CONSTRAINT pk_imc PRIMARY KEY ( id_imc )
 );

CREATE  TABLE "public".proteina (
	id_proteina          serial  NOT NULL  ,
	proteina             double precision    ,
	id_salud             bigint    ,
	CONSTRAINT pk_imc_1 PRIMARY KEY ( id_proteina )
 );

CREATE  TABLE "public".tmb (
	id_tmb               serial  NOT NULL  ,
	tmb                  double precision    ,
	id_salud             bigint    ,
	CONSTRAINT pk_imc_0 PRIMARY KEY ( id_tmb )
 );
