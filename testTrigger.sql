/*fichier destiné à montré la preuve du fonctionnement de chaque trigger
il complete insertTest.sql
*/

-- -------------------------------
-- Test d'échec : trigger verifMoinDouze
-- -------------------------------
--INSERT INTO RESERVATION (idR, idCli, dateR, nb_couverts, sur_place, statut) VALUES
--(5, 1, '2025-10-25', 11, true, 'confirmée');
--MariaDB [DBaudor]> INSERT INTO RESERVATION (idR, idCli, dateR, nb_couverts, sur_place, statut) VALUES
--    -> (5, 1, '2025-10-25', 11, true, 'confirmée');
--ERROR 1644 (45000): Pour cette journée, il y a deja 3 couverts de reserver,
--Merci de repasser demain ou de 'commander a emporter'

-- --------------------------------
-- Test de réussite : trigger initStock
-- --------------------------------
--INSERT INTO PLAT (idP, nomP, typeP, prixP, stock, stockInit, descriptionP) VALUES
--(6, 'Steack Test', 'Entrée', 8.30, 10, 0, 'Boeuf, riz');
--MariaDB [DBaudor]> select * from PLAT where idP=6;
--+-----+-------------+---------+-------+-------+-----------+--------------+
--| idP | nomP        | typeP   | prixP | stock | stockInit | descriptionP |
--+-----+-------------+---------+-------+-------+-----------+--------------+
--|   6 | Steack Test | Entrée  |  8.30 |    10 |        10 | Boeuf, riz   |
--+-----+-------------+---------+-------+-------+-----------+--------------+

-- -------------------------------
-- Test d'échec : trigger estBanniEnLigne
-- -------------------------------
--INSERT INTO RESERVATION (idR, idCli, dateR, nb_couverts, sur_place, statut) VALUES
--(7, 3, '2025-10-26', 2, false, 'en attente');
--MariaDB [DBaudor]> INSERT INTO RESERVATION (idR, idCli, dateR, nb_couverts, sur_place, statut) VALUES
--    -> (7, 3, '2025-10-26', 2, false, 'en attente');
--ERROR 1644 (45000): Vous etes sur la liste noir, il est impossible pour vous de commander en ligne,
--nous vous invitons tout de meme a commander sur place

-- -------------------------------
-- Test de reussite : trigger verifDisponibiliterPlat 1er cas (sur_place)
-- -------------------------------
--INSERT INTO PLAT (idP, nomP, typeP, prixP, stock, stockInit, descriptionP) VALUES
--(7, 'roti de test', 'Plat', 18.5, 10,0 , 'boeuf, chataigne, vin blanc');
--INSERT INTO FORMULE (idF, nomF, prixF) VALUES
--(4, 'menu viande',25);
--INSERT INTO COMPOSER (idF, idP, quantiteC) VALUES
--(4, 7, 2);
--INSERT INTO RESERVATION (idR, idCli, dateR, nb_couverts, sur_place, statut) VALUES
--(5, 1, '2025-10-26', 2, true, 'en attente');
--INSERT INTO CONTENIR_F (idR, idF, quantiteF) VALUES
--(5, 4, 2);
--On constate la modification de stock:
--MariaDB [DBaudor]> select * from PLAT where idP=7;
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+
--| idP | nomP         | typeP | prixP | stock | stockInit | descriptionP                |
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+
--|   7 | roti de test | Plat  | 18.50 |     6 |        10 | boeuf, chataigne, vin blanc |
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+
--INSERT INTO CONTENIR_P (idR, idP, quantiteP) VALUES
--(5, 7, 6);
--MariaDB [DBaudor]> select * from PLAT where idP=7;
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+
--| idP | nomP         | typeP | prixP | stock | stockInit | descriptionP                |
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+
--|   7 | roti de test | Plat  | 18.50 |     0 |        10 | boeuf, chataigne, vin blanc |
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+

--On constate que l'on ne peut plus ajouter de plat
--UPDATE CONTENIR_P set quantiteP = quantiteP+1 where idP=7 and idR=5;
--MariaDB [DBaudor]> UPDATE CONTENIR_P set quantiteP = quantiteP+1 where idP=7 and idR=5;
--ERROR 1644 (45000): Le plat d'id 7 n'a pas assez de stock pour votre commande.
--Il reste 0 unités en stock, et vous demandez 1 en plus .
--Merci de revoir votre commande.

--On constate que l'on peut enlever un plat
--UPDATE CONTENIR_P set quantiteP = quantiteP-1 where idP=7 and idR=5;
--MariaDB [DBaudor]> select * from PLAT where idP=7;
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+
--| idP | nomP         | typeP | prixP | stock | stockInit | descriptionP                |
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+
--|   7 | roti de test | Plat  | 18.50 |     1 |        10 | boeuf, chataigne, vin blanc |
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+

--on constate que l'on peut supprimer tout les plats
--delete from  CONTENIR_P where idP=7 and idR=5;
--MariaDB [DBaudor]> select * from PLAT where idP=7;
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+
--| idP | nomP         | typeP | prixP | stock | stockInit | descriptionP                |
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+
--|   7 | roti de test | Plat  | 18.50 |     6 |        10 | boeuf, chataigne, vin blanc |
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+

--On constate que l'on ne peut ajouter des formules
--UPDATE CONTENIR_F set quantiteF = quantiteF+3 where idF=4 and idR=5;
--MariaDB [DBaudor]> select * from PLAT where idP=7;
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+
--| idP | nomP         | typeP | prixP | stock | stockInit | descriptionP                |
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+
--|   7 | roti de test | Plat  | 18.50 |     0 |        10 | boeuf, chataigne, vin blanc |
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+

--On constate que l'on ne peut plus ajouter de formule;
--UPDATE CONTENIR_F set quantiteF = quantiteF+1 where idF=4 and idR=5;
--MariaDB [DBaudor]> UPDATE CONTENIR_F set quantiteF = quantiteF+1 where idF=4 and idR=5;
--ERROR 1644 (45000): Le plat d'id 7 n'a pas assez de stock pour votre commande.
--Il reste 0 unités en stock, et vous demandez 2 en plus .
--Merci de revoir votre commande.

--On constate que l'on peut supprimer toutes les formules (ou un certain nombre)
--delete from  CONTENIR_F where idF=4 and idR=5;
--MariaDB [DBaudor]> select * from PLAT where idP=7;
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+
--| idP | nomP         | typeP | prixP | stock | stockInit | descriptionP                |
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+
--|   7 | roti de test | Plat  | 18.50 |    10 |        10 | boeuf, chataigne, vin blanc |
--+-----+--------------+-------+-------+-------+-----------+-----------------------------+


-- -------------------------------
-- Test d'échec : trigger verifDisponibiliterPlat 2eme cas (en ligne)
-- -------------------------------

--INSERT INTO PLAT (idP, nomP, typeP, prixP, stock, stockInit, descriptionP) VALUES
--(8, 'dinde de test', 'Plat', 15.5, 10,0 , 'dinde, epice , pomme de terre');
--INSERT INTO FORMULE (idF, nomF, prixF) VALUES
--(5, 'menu volaille',20);
--INSERT INTO COMPOSER (idF, idP, quantiteC) VALUES
--(5, 8, 2);
--INSERT INTO RESERVATION (idR, idCli, dateR, nb_couverts, sur_place, statut) VALUES
--(6, 1, '2025-10-27', 2, false, 'en attente');

--On constate que l'on ne pas pas commander plus de 80 % du stock en ligne
--INSERT INTO CONTENIR_P (idR, idP, quantiteP) VALUES
--(6, 8, 9);
--MariaDB [DBaudor]> INSERT INTO CONTENIR_P (idR, idP, quantiteP) VALUES
--    -> (6, 8, 9);
--ERROR 1644 (45000): Le plat d id 8 n a pas assez de stock pour votre commande.
--Il reste 10 unités en stock,
--et vous en demandez 9.
--Merci de revoir votre commande.

--On constate que celui la fonctionne
--INSERT INTO CONTENIR_P (idR, idP, quantiteP) VALUES
--(6, 8, 8);

--On constate que la modification ne focntionne pas
--update CONTENIR_P set quantiteP = quantiteP + 1 where idP=8 and idR=6
--MariaDB [DBaudor]> update CONTENIR_P set quantiteP = quantiteP + 1 where idP=8 and idR=6
--    -> ;
--ERROR 1644 (45000): Le plat d'id 8 n'a pas assez de stock pour votre commande.
--Il reste 2 unités en stock, et vous demandez 1 en plus .
--Merci de revoir votre commande.

--On constate le meme fonctionnement pour les formules: ( j'ai reset le stock a 10)
--INSERT INTO CONTENIR_F (idR, idF, quantiteF) VALUES
--(6, 5, 5);
--MariaDB [DBaudor]> INSERT INTO CONTENIR_F (idR, idF, quantiteF) VALUES
--    -> (6, 5, 5);
--ERROR 1644 (45000): Le plat d id 8 n a pas assez de stock pour votre commande.
--Il reste 10 unités en stock,
--et vous en demandez 10.
--Merci de revoir votre commande.