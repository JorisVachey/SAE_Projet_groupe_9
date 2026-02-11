drop table if EXISTS CONTENIR_P;
drop table if EXISTS CONTENIR_F;
drop table if EXISTS CONTENIR_R;
drop table if EXISTS COMPOSER;
drop table if EXISTS FORMULE;
drop table if EXISTS PLAT;
drop table if EXISTS RESTRICTION;
drop table if EXISTS TYPE_PLAT;
drop table if EXISTS RESERVATION;
drop table if EXISTS USER;

    create table USER (
        idUser int,
        numtelUser varchar(50) unique,
        pseudonyme varchar(50),
        mdp varchar(500),
        est_banni boolean,
        pts_fidelite int,
        est_admin boolean,
        PRIMARY KEY (idUser)
    );

    ALTER TABLE USER MODIFY idUser INT NOT NULL AUTO_INCREMENT;

    create table RESERVATION (
        idR int,
        idUser int,
        dateR date,
        nb_couverts int,
        sur_place boolean,
        statut varchar(50),
        PRIMARY KEY (idR,idUser)
    );

    ALTER TABLE RESERVATION MODIFY idR INT NOT NULL AUTO_INCREMENT;
    ALTER TABLE RESERVATION ADD FOREIGN KEY (idUser) REFERENCES USER(idUser);

    create table FORMULE (
        idF int,
        nomF varchar(50),
        prixF decimal(10,2),
        cheminImg varchar(200),
        PRIMARY KEY (idF)
    );

    create table TYPE_PLAT(
        idTp int,
        nomTP varchar(50),
        descriptionTp longtext,
        cheminImg varchar(200),
        PRIMARY KEY (idTp)
    );

create table PLAT(
    idP int,
    nomP varchar(50),
    idTp int,
    prixP decimal(10,2),
    stock int,
    stockInit int,
    descriptionP longtext,
    cheminImg varchar(200),
    PRIMARY KEY (idP)
);
ALTER TABLE PLAT MODIFY idP INT NOT NULL AUTO_INCREMENT;
ALTER TABLE PLAT ADD FOREIGN KEY (idTp) REFERENCES TYPE_PLAT (idTp);

create table COMPOSER (
    idF int,
    idP int,
    quantiteC int,
    PRIMARY KEY (idF,idP)
);

    ALTER TABLE COMPOSER ADD FOREIGN KEY (idF) REFERENCES FORMULE (idF);
    ALTER TABLE COMPOSER ADD FOREIGN KEY (idP) REFERENCES PLAT (idP) ON DELETE CASCADE;

    create table CONTENIR_F(
        idF int,
        idR int,
        quantiteF int,
        PRIMARY KEY (idR,idF)
    );


ALTER TABLE CONTENIR_F ADD FOREIGN KEY (idF) REFERENCES FORMULE (idF);
ALTER TABLE CONTENIR_F ADD FOREIGN KEY (idR) REFERENCES RESERVATION (idR) ON DELETE CASCADE;


    create table CONTENIR_P (
        idP int,
        idR int,
        quantiteP int,
        PRIMARY KEY (idR,idP)
    );

ALTER TABLE CONTENIR_P ADD FOREIGN KEY (idP) REFERENCES PLAT (idP) ON DELETE CASCADE;
ALTER TABLE CONTENIR_P ADD FOREIGN KEY (idR) REFERENCES RESERVATION (idR) ON DELETE CASCADE;

    create table RESTRICTION (
        nomA varchar(50),
        PRIMARY KEY (nomA)
    );

    create table CONTENIR_R (
        idP int,
        nomA varchar(50),
        PRIMARY KEY (idP,nomA)
    );

    ALTER TABLE CONTENIR_R ADD FOREIGN KEY (idP) REFERENCES PLAT (idP) ON DELETE CASCADE;
    ALTER TABLE CONTENIR_R ADD FOREIGN KEY (nomA) REFERENCES RESTRICTION (nomA);


DELIMITER |
create or replace trigger initStock before insert on PLAT for each row
begin
    set new.stockInit = new.stock ;
end |
DELIMITER ;

DELIMITER |
create or replace trigger verifMoinDouze before insert on RESERVATION for each row
begin
    declare nbCouv int default 0;
    declare mes varchar(500) default '';
    select sum(nb_couverts) into nbCouv from RESERVATION where dateR=new.dateR and sur_place=true;
    if nbCouv+new.nb_couverts>12 then
        set mes = concat(mes,"Pour aujourd'hui, il y a deja ",nbCouv," couverts de reservés, \nMerci de repasser demain, ou de 'commander à emporter'");
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = mes;
    end if;
end |
DELIMITER ;

DELIMITER |
create or replace trigger estBanniEnLigne before insert on RESERVATION for each row
begin
    declare mes varchar(500) default '';
    declare ban boolean default false;
    if new.sur_place=false then
        select est_banni into ban from USER where idUser=new.idUser;
        if ban=true then
            set mes = concat(mes,"Vous etes sur la liste noir, il est impossible pour vous de commander en ligne, \nnous vous invitons tout de meme a commander sur place");
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = mes;
        end if;
    end if;
end |
DELIMITER ;
