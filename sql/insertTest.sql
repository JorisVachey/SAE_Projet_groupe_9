/*Voici un jeu d'insert (generer par IA) reduit ,
afin de tester la base de donnée ainsi que les triggers 
*/
INSERT INTO RESTAURATRICE (idRest, nomRest, prenomRest, numtelRest, mdp) VALUES
(1, 'Dupont', 'Marie', '0601020304', 'mdp123'),
(2, 'Martin', 'Sophie', '0605060708', 'chef2024');

INSERT INTO CLIENT (idCli, numtelCli, nomCli, prenomCli, est_banni) VALUES
(1, '0611223344', 'Durand', 'Paul', false),
(2, '0611334455', 'Lemoine', 'Claire', false),
(3, '0622445566', 'Bernard', 'Lucas', true),
(4, '0633556677', 'Petit', 'Julie', false);

INSERT INTO RESERVATION (idR, idCli, dateR, nb_couverts, sur_place, statut) VALUES
(1, 1, '2025-10-20', 2, true, 'confirmée'),
(2, 2, '2025-10-21', 4, true, 'en attente'),
(3, 4, '2025-10-22', 1, false, 'livraison'),
(4, 1, '2025-10-25', 3, true, 'annulée');

INSERT INTO FORMULE (idF, nomF, prixF) VALUES
(1, 'Menu Midi', 19.90),
(2, 'Menu Dégustation', 39.90),
(3, 'Menu Enfant', 9.90);

INSERT INTO PLAT (idP, nomP, typeP, prixP, stock, stockInit, descriptionP) VALUES
(1, 'Salade César', 'Entrée', 7.50, 20, 20, 'Salade, poulet, parmesan'),
(2, 'Boeuf Bourguignon', 'Plat', 14.90, 15, 15, 'Boeuf mijoté au vin rouge'),
(3, 'Tarte aux pommes', 'Dessert', 5.50, 10, 10, 'Tarte maison'),
(4, 'Soupe du jour', 'Entrée', 6.00, 12, 12, 'Velouté de saison'),
(5, 'Pâtes carbonara', 'Plat', 13.50, 18, 18, 'Crème, lardons, parmesan');

INSERT INTO COMPOSER (idF, idP, quantiteC) VALUES
(1, 1, 1),
(1, 5, 1),
(1, 3, 1),
(2, 4, 1),
(2, 2, 1),
(2, 3, 1),
(3, 5, 1),
(3, 3, 1);

INSERT INTO CONTENIR_F (idR, idF, quantiteF) VALUES
(1, 1, 2),
(2, 2, 4),
(3, 3, 1);

INSERT INTO CONTENIR_P (idR, idP, quantiteP) VALUES
(1, 2, 1),
(1, 3, 1),
(2, 4, 2),
(3, 5, 1),
(4, 1, 2);
