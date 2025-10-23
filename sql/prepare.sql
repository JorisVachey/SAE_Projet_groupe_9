/* permet de recuperer l'id du plat ainsi que sa quantité, en fonction d'une reservation*/
PREPARE QteTotale FROM
'SELECT idP, SUM(quantite) AS quantite_totale
 FROM (
     SELECT idP, quantiteP AS quantite
     FROM CONTENIR_P
     WHERE idR = ?
     UNION ALL
     SELECT idP, (quantiteF * quantiteC) AS quantite
     FROM CONTENIR_F
     NATURAL JOIN COMPOSER
     WHERE idR = ?
 ) AS q
 GROUP BY idP';

