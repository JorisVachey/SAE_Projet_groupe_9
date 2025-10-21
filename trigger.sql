/* initialise les valeurs de quantité du stock des plats,
afin de pouvoir calculer 80% du stock total  */

DELIMITER |
create or replace trigger initStock before insert on PLAT for each row
begin
    set new.stockInit = new.stock ;
end |
DELIMITER ;

/* permet de definir une limite de couvert par jour à 12
*/
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

/* permet de verifier avant l'ajout d'un plat (ou formule),
sachant que la reservation est en ligne,
qu'il restera au minimum 20 % du stock initial de la journée
permet de verifier pour chaque reservation (sur place ou non)
si la quantité de plat ne depasse pas le stock du restaurant
*/
DELIMITER |
create or replace trigger verifDisponibiliterPlatUnique before insert on CONTENIR_P for each row
begin
    DECLARE mes VARCHAR(500) DEFAULT '';
    DECLARE variableChoixCom DECIMAL(3,2) DEFAULT 1;
    DECLARE quantiteStock INT;
    DECLARE quantiteInit INT;
    declare place boolean default false;
    select sur_place into place from RESERVATION where idR=new.idR;
    SELECT stock, stockInit INTO quantiteStock, quantiteInit
        FROM PLAT
        WHERE idP = new.idP;
    if place=false then
        set variableChoixCom=0.8;
    end if;
    IF new.quantiteP > quantiteStock OR new.quantiteP > quantiteInit * variableChoixCom THEN
        set mes = concat(mes,"Le plat d id ",new.idP," n a pas assez de stock pour votre commande. \nIl reste ",quantiteStock," unités en stock, \net vous en demandez ",new.quantiteP,".\nMerci de revoir votre commande.");
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = mes;
    end if ;
end|
DELIMITER ;

DELIMITER |
create or replace trigger verifDisponibiliterPlatUniqueUpdate before UPDATE on CONTENIR_P for each row
begin
    declare mes varchar(500) default '';
    declare variableChoixCom DECIMAL(3,2) default 1;
    declare idPlat int;
    declare quantiteStock int;
    declare quantiteInit int;
    declare qteDemande int;
    declare fini boolean default false;
    declare place boolean default false;
    select sur_place into place from RESERVATION where idR=new.idR;
    if place=false then
        set variableChoixCom=0.8;
    end if;
    set qteDemande = NEW.quantiteP - OLD.quantiteP;
    IF qteDemande > 0 THEN
        SELECT stock, stockInit INTO quantiteStock, quantiteInit
        FROM PLAT
        WHERE idP = NEW.idP;
        IF (qteDemande > quantiteStock or NEW.quantiteP > quantiteInit * variableChoixCom) THEN
            set mes = CONCAT(
                "Le plat d'id ", NEW.idP,
                " n'a pas assez de stock pour votre commande.\nIl reste ",
                quantiteStock, " unités en stock, et vous demandez ",
                qteDemande, " en plus .\nMerci de revoir votre commande."
            );
            SIGNAL SQLSTATE '45000' set MESSAGE_TEXT = mes;
        END IF;
    END IF;
end|
DELIMITER ;

/* on met a jour le stock après avoir ajouter,modifier ou supprimer des plats des plats, si ils sont validés
*/
DELIMITER |
CREATE OR REPLACE TRIGGER majStockPlatUnique AFTER INSERT ON CONTENIR_P FOR EACH ROW
BEGIN
    UPDATE PLAT SET stock = stock - new.quantiteP WHERE idP = new.idP;
END|
DELIMITER ;

DELIMITER |
CREATE OR REPLACE TRIGGER majStockPlatUniqueUpdate AFTER UPDATE ON CONTENIR_P FOR EACH ROW
BEGIN
    UPDATE PLAT SET stock = stock - (new.quantiteP - old.quantiteP) WHERE idP = new.idP;
END|
DELIMITER ;

DELIMITER |
CREATE OR REPLACE TRIGGER majStockPlatUniqueDelete AFTER delete ON CONTENIR_P FOR EACH ROW
BEGIN
    UPDATE PLAT SET stock = stock + old.quantiteP WHERE idP = old.idP;
END|
DELIMITER ;

/*meme chose pour l'autre table
*/

DELIMITER |
create or replace trigger verifDisponibiliterPlatForm before insert on CONTENIR_F for each row
begin
    declare mes varchar(500) default '';
    declare variableChoixCom DECIMAL(3,2) default 1;
    declare idPlat int;
    declare quantiteStock int;
    declare quantiteInit int;
    declare qteDemande int;
    declare fini boolean default false;
    declare place boolean default false;
    DECLARE platUnique CURSOR FOR
        SELECT idP, quantiteC * NEW.quantiteF AS qteDemande
        FROM COMPOSER
        WHERE idF = NEW.idF;
    declare continue HANDLER for not found set fini = TRUE;
    select sur_place into place from RESERVATION where idR=new.idR;
    if place=false then
        set variableChoixCom=0.8;
    end if;
    open platUnique ;
    while not fini do
        if not fini then
            fetch platUnique into idPlat,qteDemande ;
            select stock, stockInit into quantiteStock, quantiteInit from PLAT where idP=idPlat ;
            IF qteDemande > quantiteStock or qteDemande > quantiteInit * variableChoixCom then
                set mes = concat(mes,"Le plat d id ",idPlat," n a pas assez de stock pour votre commande. \nIl reste ",quantiteStock," unités en stock, \net vous en demandez ",qteDemande,".\nMerci de revoir votre commande.");
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = mes;
            end if ;
        end if ;
    end while ;
    close platUnique ;
end|
DELIMITER ;

DELIMITER |
create or replace trigger verifDisponibiliterPlatFormUpdate before UPDATE on CONTENIR_F for each row
begin
    declare mes varchar(500) default '';
    declare variableChoixCom DECIMAL(3,2) default 1;
    declare idPlat int;
    declare quantiteStock int;
    declare quantiteInit int;
    declare qteDemande int;
    declare fini boolean default false;
    declare place boolean default false;
    declare qteEnCours int default 0;
    declare qteAncien CURSOR for
        SELECT idP, old.quantiteF * quantiteC AS qte_diff
        FROM COMPOSER
        WHERE idF = new.idF;
    declare platUnique CURSOR FOR
        SELECT idP, (new.quantiteF - old.quantiteF) * quantiteC AS qte_diff
        FROM COMPOSER
        WHERE idF = new.idF;
    declare continue HANDLER for not found set fini = TRUE;
    select sur_place into place from RESERVATION where idR=new.idR;
    if place=false then
        set variableChoixCom=0.8;
    end if;
    open platUnique ;
    while not fini do
        if not fini then
            fetch platUnique into idPlat,qteDemande ;
            fetch qteAncien into qteEnCours;
            IF qteDemande > 0 THEN
                SELECT stock, stockInit INTO quantiteStock, quantiteInit
                FROM PLAT
                WHERE idP = idPlat;
                IF (qteDemande > quantiteStock or qteDemande+qteEnCours > quantiteInit * variableChoixCom) THEN
                    set mes = CONCAT(
                        "Le plat d'id ", idPlat,
                        " n'a pas assez de stock pour votre commande.\nIl reste ",
                        quantiteStock, " unités en stock, et vous demandez ",
                        qteDemande, " en plus .\nMerci de revoir votre commande."
                    );
                    SIGNAL SQLSTATE '45000' set MESSAGE_TEXT = mes;
                END IF;
            END IF;
        end if;
    end while;
    close platUnique;
end|
DELIMITER ;

/*meme chose avec les formules
*/

DELIMITER |
CREATE OR REPLACE TRIGGER majStockPlatForm AFTER INSERT ON CONTENIR_F FOR EACH ROW
BEGIN
    UPDATE PLAT NATURAL JOIN COMPOSER SET stock = stock - (new.quantiteF * quantiteC) WHERE idF = new.idF;
END|
DELIMITER ;

DELIMITER |
CREATE OR REPLACE TRIGGER majStockPlatFormUpdate AFTER UPDATE ON CONTENIR_F FOR EACH ROW
BEGIN
    UPDATE PLAT NATURAL JOIN COMPOSER SET stock = stock - ((new.quantiteF - old.quantiteF) * quantiteC) WHERE idF = new.idF;
END|
DELIMITER ;

DELIMITER |
CREATE OR REPLACE TRIGGER majStockPlatFormDelete AFTER delete ON CONTENIR_F FOR EACH ROW
BEGIN
    UPDATE PLAT NATURAL JOIN COMPOSER SET stock = stock + (old.quantiteF * quantiteC) WHERE idF = old.idF;
END|
DELIMITER ;


/* permet de verifier le refus de reservation en ligne pour un client banni du restaurant
*/
DELIMITER |
create or replace trigger estBanniEnLigne before insert on RESERVATION for each row
begin
    declare mes varchar(500) default '';
    declare ban boolean default false;
    if new.sur_place=false then
        select est_banni into ban from CLIENT where idCli=new.idCli;
        if ban=true then
            set mes = concat(mes,"Vous etes sur la liste noir, il est impossible pour vous de commander en ligne, \nnous vous invitons tout de meme a commander sur place");
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = mes;
        end if;
    end if;
end |
DELIMITER ;

