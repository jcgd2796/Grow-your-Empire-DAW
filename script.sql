--
-- Create model Question
--
CREATE TABLE DAWActivity_question (questionText varchar(100) NOT NULL PRIMARY KEY, questionOption1 varchar(100) NOT NULL, questionOption2 varchar(100) NOT NULL, questionOption3 varchar(100) NOT NULL, questionOption4 varchar(100) NOT NULL, testName_id varchar(100) NOT NULL REFERENCES DAWActivity_test (testName) , correctOption varchar(1) NOT NULL);
--
-- Create model Test
--
CREATE TABLE DAWActivity_test (subject integer NOT NULL, testName varchar(100) NOT NULL PRIMARY KEY, date datetime NOT NULL);
--
-- Create model Village
--
CREATE TABLE DAWActivity_village (villageName varchar(100) NOT NULL PRIMARY KEY, dailyFood integer NOT NULL, dailyWood integer NOT NULL, dailyStone integer NOT NULL, storedFood integer NOT NULL, storedWood integer NOT NULL, storedStone integer NOT NULL, foodLevel integer NOT NULL, woodLevel integer NOT NULL, stoneLevel integer NOT NULL, wallLevel integer NOT NULL, storageLevel integer NOT NULL, soldiers integer NOT NULL, owner_id integer NOT NULL REFERENCES auth_user (id) );
--
-- Create model Upgrade
--
CREATE TABLE DAWActivity_upgrade (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, building integer NOT NULL, woodCost integer NOT NULL, stoneCost integer NOT NULL, completed bool NOT NULL, village_id varchar(100) NOT NULL REFERENCES DAWActivity_village (villageName) , level integer NOT NULL);
--
-- Create model Training
--
CREATE TABLE DAWActivity_training (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, completed bool NOT NULL, units integer NOT NULL, foodCost integer NOT NULL, village_id varchar(100) NOT NULL REFERENCES DAWActivity_village (villageName) );
--
-- Create model TradeOffer
--
CREATE TABLE DAWActivity_tradeoffer (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, wants integer NOT NULL, wantsResource varchar(100) NOT NULL, accepted bool NOT NULL, destination_id varchar(100) NOT NULL REFERENCES DAWActivity_village (villageName) , source_id varchar(100) NOT NULL REFERENCES DAWActivity_village (villageName) );
--
-- Create model TestResolution
--
CREATE TABLE DAWActivity_testresolution (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, points integer NOT NULL, testName_id varchar(100) NOT NULL REFERENCES DAWActivity_test (testName) , userName_id integer NOT NULL REFERENCES auth_user (id) );
--
-- Create model Attack
--
CREATE TABLE DAWActivity_attack (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, completed bool NOT NULL, usedSoldiers integer NOT NULL, registeredDateTime datetime NOT NULL, attacker_id varchar(100) NOT NULL REFERENCES DAWActivity_village (villageName) , defendant_id varchar(100) NOT NULL REFERENCES DAWActivity_village (villageName) );
--
-- Create model Activity
--
CREATE TABLE DAWActivity_activity (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, activityText varchar(100) NOT NULL, activityDate date NOT NULL, owner_id varchar(100) NOT NULL REFERENCES DAWActivity_village (villageName) );
--
-- Create model Bonus
--
CREATE TABLE DAWActivity_bonus (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, bonusType integer NOT NULL, bonusAmount integer NOT NULL, completed bool NOT NULL, village_id varchar(100) NOT NULL REFERENCES DAWActivity_village (villageName) );
--
-- Create model Student
--
CREATE TABLE DAWActivity_student (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, subject integer NOT NULL, user_id integer NOT NULL UNIQUE REFERENCES auth_user (id) );
COMMIT;
BEGIN;

CREATE INDEX DAWActivity_village_owner_id_6499c7d7 ON DAWActivity_village (owner_id);
CREATE INDEX DAWActivity_upgrade_village_id_408dce79 ON DAWActivity_upgrade (village_id);
CREATE INDEX DAWActivity_training_village_id_12790a97 ON DAWActivity_training (village_id);
CREATE INDEX DAWActivity_testresolution_testName_id_05f09d8c ON DAWActivity_testresolution (testName_id);
CREATE INDEX DAWActivity_testresolution_userName_id_eeebd4bb ON DAWActivity_testresolution (userName_id);
CREATE INDEX DAWActivity_attack_attacker_id_c3b71c8c ON DAWActivity_attack (attacker_id);
CREATE INDEX DAWActivity_attack_defendant_id_00414ff1 ON DAWActivity_attack (defendant_id);
CREATE INDEX DAWActivity_question_testName_id_41568988 ON DAWActivity_question (testName_id);
CREATE INDEX DAWActivity_tradeoffer_source_id_34c879b6 ON DAWActivity_tradeoffer (source_id);
CREATE INDEX DAWActivity_activity_owner_id_909668dc ON DAWActivity_activity (owner_id);
CREATE INDEX DAWActivity_tradeoffer_destination_id_2fd74c8a ON DAWActivity_tradeoffer (destination_id);
CREATE INDEX DAWActivity_tradeoffer_source_id_34c879b6 ON DAWActivity_tradeoffer (source_id);
CREATE INDEX DAWActivity_bonus_village_id_8b96b70f ON DAWActivity_bonus (village_id);
COMMIT;
