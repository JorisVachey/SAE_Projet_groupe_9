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
create or replace trigger verifDisponibiliterPlat before insert on RESERVATION for each row
begin
    declare mes varchar(500) default '';
    declare variableChoixCom DECIMAL(3,2) default 1;
    declare idPlat int;
    declare quantiteStock int;
    declare quantiteInit int;
    declare qteDemande int;
    declare fini boolean default false;
    declare platUnique cursor for
        SELECT idP, SUM(quantite) AS quantite_totale
        FROM (
            SELECT idP, quantiteP AS quantite
            FROM CONTENIR_P
            WHERE idR = new.idR
            UNION ALL
            SELECT idP, (quantiteF * quantiteC) AS quantite
            FROM CONTENIR_F
            NATURAL JOIN COMPOSER
            WHERE idR = new.idR
        ) AS q
        GROUP BY idP;
    declare continue HANDLER for not found set fini = TRUE;
    if new.sur_place=false then
        set variableChoixCom=0.8;
    end if;
    open platUnique ;
    while not fini do
        if not fini then
            fetch platUnique into idPlat,qteDemande ;
            select stock, stockInit into quantiteStock, quantiteInit from PLAT where idP=idPlat ;
            if (qteDemande > quantiteInit*variableChoixCom OR qteDemande>quantiteStock) then
                set mes = concat(mes,"Le plat d id ",idPlat," n a pas assez de stock pour votre commande. \nIl reste ",quantiteStock," unités en stock, \net vous en demandez ",qteDemande,".\nMerci de revoir votre commande.");
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = mes;
            end if ;
        end if ;
    end while ;
    close platUnique ;
end|
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

