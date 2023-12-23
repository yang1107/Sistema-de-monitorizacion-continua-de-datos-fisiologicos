create extension if not exists timescaledb cascade;
select create_hypertable('entrenamiento','date_entrenamiento');
select create_hypertable('elevacion_entrenamiento','time_elevacion');
select create_hypertable('distancia_entrenamiento','time_distancia');
select create_hypertable('pasos_entrenamiento','time_pasos');
select create_hypertable('calorias_entrenamiento','time_calorias');
select create_hypertable('hr_entrenamiento','time_hr');
select create_hypertable('spo2_average_entrenamiento','time_spo2');
select create_hypertable('hr_suenio','time_hr');
select create_hypertable('senial_ecg','time_senial');
select create_hypertable('distancia','time_distancia');
select create_hypertable('heart_rate','time_heart_rate');
select create_hypertable('spo2','time_spo2');
select create_hypertable('elevacion','time_elevacion');
select create_hypertable('pasos','time_pasos');
select create_hypertable('calorias','time_calorias');

