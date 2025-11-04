create table RESTAURATRICE (
    idRest int,
    nomRest varchar(50),
    prenomRest varchar(50),
    numtelRest varchar(50),
    mdp varchar(500),
    PRIMARY KEY (idRest)
);

create table CLIENT (
    numtelCli varchar(50),
    pseudonyme varchar(50),
    mdp varchar(500),
    est_banni boolean,
    pts_fidelite int,
    PRIMARY KEY (numtelCli)

);

create table RESERVATION (
    idR int,
    numtelCli varchar(50),
    dateR date,
    nb_couverts int,
    sur_place boolean,
    statut varchar(50),
    PRIMARY KEY (idR,numtelCli)
);

ALTER TABLE RESERVATION ADD FOREIGN KEY (numtelCli) REFERENCES CLIENT(numtelCli);

create table FORMULE (
    idF int,
    nomF varchar(50),
    prixF decimal(10,2),
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

ALTER TABLE PLAT ADD FOREIGN KEY (idTp) REFERENCES TYPE_PLAT (idTp);

create table COMPOSER (
    idF int,
    idP int,
    quantiteC int,
    PRIMARY KEY (idF,idP)
);

ALTER TABLE COMPOSER ADD FOREIGN KEY (idF) REFERENCES FORMULE (idF);
ALTER TABLE COMPOSER ADD FOREIGN KEY (idP) REFERENCES PLAT (idP);

create table CONTENIR_F(
    idF int,
    idR int,
    quantiteF int,
    PRIMARY KEY (idR,idF)
);

ALTER TABLE CONTENIR_F ADD FOREIGN KEY (idF) REFERENCES FORMULE (idF);
ALTER TABLE CONTENIR_F ADD FOREIGN KEY (idR) REFERENCES RESERVATION (idR);

create table CONTENIR_P (
    idP int,
    idR int,
    quantiteP int,
    PRIMARY KEY (idR,idP)
);

ALTER TABLE CONTENIR_P ADD FOREIGN KEY (idR) REFERENCES RESERVATION (idR);
ALTER TABLE CONTENIR_P ADD FOREIGN KEY (idP) REFERENCES PLAT (idP);

