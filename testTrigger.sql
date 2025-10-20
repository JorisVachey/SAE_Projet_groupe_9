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
-- Test d'échec : trigger verifDisponibiliterPlat
-- -------------------------------