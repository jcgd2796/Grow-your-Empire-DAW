--
-- Create model Question
--
CREATE TABLE question (questionText varchar(100) NOT NULL PRIMARY KEY, questionOption1 varchar(100) NOT NULL, questionOption2 varchar(100) NOT NULL, questionOption3 varchar(100) NOT NULL, questionOption4 varchar(100) NOT NULL, testName_id varchar(100) NOT NULL REFERENCES test (testName) , correctOption varchar(1) NOT NULL);
--
-- Create model Test
--
CREATE TABLE test (subject integer NOT NULL, testName varchar(100) NOT NULL PRIMARY KEY, date datetime NOT NULL);
--
-- Create model Village
--
CREATE TABLE village (villageName varchar(100) NOT NULL PRIMARY KEY, dailyFood integer NOT NULL, dailyWood integer NOT NULL, dailyStone integer NOT NULL, storedFood integer NOT NULL, storedWood integer NOT NULL, storedStone integer NOT NULL, foodLevel integer NOT NULL, woodLevel integer NOT NULL, stoneLevel integer NOT NULL, wallLevel integer NOT NULL, storageLevel integer NOT NULL, soldiers integer NOT NULL, owner_id integer NOT NULL REFERENCES auth_user (id) );
--
-- Create model Upgrade
--
CREATE TABLE upgrade (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, building integer NOT NULL, woodCost integer NOT NULL, stoneCost integer NOT NULL, completed bool NOT NULL, village_id varchar(100) NOT NULL REFERENCES village (villageName) , level integer NOT NULL);
--
-- Create model Training
--
CREATE TABLE training (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, completed bool NOT NULL, units integer NOT NULL, foodCost integer NOT NULL, village_id varchar(100) NOT NULL REFERENCES village (villageName) );
--
-- Create model TradeOffer
--
CREATE TABLE tradeoffer (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, wants integer NOT NULL, wantsResource varchar(100) NOT NULL, accepted bool NOT NULL, destination_id varchar(100) NOT NULL REFERENCES village (villageName) , source_id varchar(100) NOT NULL REFERENCES village (villageName) );
--
-- Create model TestResolution
--
CREATE TABLE testresolution (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, points integer NOT NULL, testName_id varchar(100) NOT NULL REFERENCES test (testName) , userName_id integer NOT NULL REFERENCES auth_user (id) );
--
-- Create model Attack
--
CREATE TABLE attack (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, completed bool NOT NULL, usedSoldiers integer NOT NULL, registeredDateTime datetime NOT NULL, attacker_id varchar(100) NOT NULL REFERENCES village (villageName) , defendant_id varchar(100) NOT NULL REFERENCES village (villageName) );
--
-- Create model Activity
--
CREATE TABLE activity (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, activityText varchar(100) NOT NULL, activityDate date NOT NULL, owner_id varchar(100) NOT NULL REFERENCES village (villageName) );
--
-- Create model Bonus
--
CREATE TABLE bonus (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, bonusType integer NOT NULL, bonusAmount integer NOT NULL, completed bool NOT NULL, village_id varchar(100) NOT NULL REFERENCES village (villageName) );
--
-- Create model Student
--
CREATE TABLE student (student_id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, subject integer NOT NULL, username varchar (100) NOT NULL, password varchar(250) NOT NULL, disabled bool NOT NULL, lastLogin datetime);
--
-- Create model New
--
CREATE TABLE new (new_id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, title varchar (100) NOT NULL,content varchar(1000), publishDate datetime NOT NULL);
COMMIT;
BEGIN;

CREATE INDEX village_owner_id ON village (owner_id);
CREATE INDEX upgrade_village_id ON upgrade (village_id);
CREATE INDEX training_village_id ON training (village_id);
CREATE INDEX testresolution_testName_id ON testresolution (testName_id);
CREATE INDEX testresolution_userName_id ON testresolution (userName_id);
CREATE INDEX attack_attacker_id ON attack (attacker_id);
CREATE INDEX attack_defendant_id ON attack (defendant_id);
CREATE INDEX question_testName_id ON question (testName_id);
CREATE INDEX activity_owner_id ON activity (owner_id);
CREATE INDEX tradeoffer_destination_id ON tradeoffer (destination_id);
CREATE INDEX tradeoffer_source_id ON tradeoffer (source_id);
CREATE INDEX bonus_village_id ON bonus (village_id);
CREATE INDEX student_id ON student(student_id);
CREATE INDEX new_id ON new(new_id)
COMMIT;
