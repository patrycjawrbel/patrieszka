-- sqlite3 library.db < library-schema.sql
drop table if exists classes;
create table if not exists classes (
    id_class integer primary key,
    class_name text not null
);

drop table if exists predictions;
create table if not exists predictions (
    id_pred integer primary key,
    photo_name text not null,
    apple real default 0,
    banana real default 0,
    lemon real default 0,
    orange real default 0,
    pear real default 0,
    carrot real default 0,
    cucumber real default 0,
    pepper real default 0,
    potato real default 0,
    tomato real default 0
);

drop table if exists labels;
create table if not exists labels (
    id_pred integer,
    id_class integer,
    primary key(id_pred, id_class),
    foreign key(id_pred)
        references predictions(id_pred)
            on delete no action,
    foreign key(id_class)
        references classes(id_class)
            on delete cascade
);


