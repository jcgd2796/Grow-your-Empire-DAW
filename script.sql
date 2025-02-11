--
-- Create model Student
--
CREATE TABLE `GrowYourEmpire_student` (`user_id` VARCHAR(150) NOT NULL PRIMARY KEY);
--
-- Create model Subject
--
CREATE TABLE `GrowYourEmpire_subject` (`subjectName` VARCHAR(100) NOT NULL PRIMARY KEY);
--
-- Create model New
--
CREATE TABLE `GrowYourEmpire_new` (`id` BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` VARCHAR(100) NOT NULL, `desc` VARCHAR(2000) NOT NULL, `registeredDateTime` datetime(6) NOT NULL, CONSTRAINT `New_title_registeredDateTime` UNIQUE (`title`, `registeredDateTime`));
--
-- Create model Village
--
CREATE TABLE `GrowYourEmpire_village` (`villageName` VARCHAR(50) NOT NULL, `dailyFood` INTEGER NOT NULL, `dailyWood` INTEGER NOT NULL, `dailyStone` INTEGER NOT NULL, `storedFood` INTEGER NOT NULL, `storedWood` INTEGER NOT NULL, `storedStone` INTEGER NOT NULL, `foodLevel` INTEGER NOT NULL, `woodLevel` INTEGER NOT NULL, `stoneLevel` INTEGER NOT NULL, `wallLevel` INTEGER NOT NULL, `storageLevel` INTEGER NOT NULL, `soldiers` INTEGER NOT NULL, `lastLogin` date NOT NULL, `disabled` bool NOT NULL, `owner_id` VARCHAR(150) NOT NULL PRIMARY KEY, 'major_god' VARCHAR(20));
--
-- Add field subject to student
--
CREATE TABLE `GrowYourEmpire_student_subject` (`id` BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY, `student_id` VARCHAR(150) NOT NULL, `subject_id` VARCHAR(100) NOT NULL);
--
-- Create model Test
--
CREATE TABLE `GrowYourEmpire_test` (`id` BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY, `testName` VARCHAR(50) NOT NULL, `date` datetime(6) NOT NULL, `subject_id` VARCHAR(100) NOT NULL);
--
-- Create model Question
--
CREATE TABLE `GrowYourEmpire_question` (`id` BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY, `questionText` VARCHAR(50) NOT NULL, `expectedText` VARCHAR(100) NOT NULL, `questionType` VARCHAR(50) NOT NULL, `testName_id` VARCHAR(50) NOT NULL);
--
-- Create model TestResolution
--
CREATE TABLE `GrowYourEmpire_testresolution` (`id` BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY, `points` INTEGER NOT NULL, `studentName_id` VARCHAR(150) NOT NULL, `testName_id` VARCHAR(50) NOT NULL);
--
-- Create model Option
--
CREATE TABLE `GrowYourEmpire_option` (`id` BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY, `questionOptionText` VARCHAR(50) NOT NULL, `correctOption` bool NOT NULL, `questionText_id` BIGINT NOT NULL, CONSTRAINT `Option_questionText_questionOptionText` UNIQUE (`questionOptionText`, `questionText_id`));
--
-- Create model Upgrade
--
CREATE TABLE `GrowYourEmpire_upgrade` (`id` BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY, `registeredDateTime` datetime(6) NOT NULL, `level` INTEGER NOT NULL, `building` INTEGER NOT NULL, `woodCost` INTEGER NOT NULL, `stoneCost` INTEGER NOT NULL, `completed` bool NOT NULL, `village_id` VARCHAR(150) NOT NULL);
--
-- Create model Training
--
CREATE TABLE `GrowYourEmpire_training` (`id` BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY, `registeredDateTime` datetime(6) NOT NULL, `units` INTEGER NOT NULL, `foodCost` INTEGER NOT NULL, `completed` bool NOT NULL, `village_id` VARCHAR(150) NOT NULL);
--
-- Create model TradeOffer
--
CREATE TABLE `GrowYourEmpire_tradeoffer` (`id` BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY, `registeredDateTime` datetime(6) NOT NULL, `wantedWood` INTEGER NOT NULL, `wantedFood` INTEGER NOT NULL, `wantedStone` INTEGER NOT NULL, `offeredWood` INTEGER NOT NULL, `offeredFood` INTEGER NOT NULL, `offeredStone` INTEGER NOT NULL, `accepted` bool NOT NULL, `destination_id` VARCHAR(150) NOT NULL, `source_id` VARCHAR(150) NOT NULL);
--
-- Create model Bonus
--
CREATE TABLE `GrowYourEmpire_bonus` (`id` BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY, `registeredDateTime` datetime(6) NOT NULL, `bonusType` INTEGER NOT NULL, `bonusAmount` INTEGER NOT NULL, `completed` bool NOT NULL, `village_id` VARCHAR(150) NOT NULL);
--
-- Create model Attack
--
CREATE TABLE `GrowYourEmpire_attack` (`id` BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY, `usedSoldiers` INTEGER NOT NULL, `registeredDateTime` datetime(6) NOT NULL, `completed` bool NOT NULL, `attacker_id` VARCHAR(150) NOT NULL, `defendant_id` VARCHAR(150) NOT NULL);
--
-- Create model Activity
--
CREATE TABLE `GrowYourEmpire_activity` (`id` BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY, `activityText` VARCHAR(150) NOT NULL, `activityDate` datetime(6) NOT NULL, `owner_id` VARCHAR(150) NOT NULL);
--
-- Create model Event
--
CREATE TABLE `GrowYourEmpire_event` ('id' BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY, 'title' VARCHAR(50), description VARCHAR(1000), startDate DATE, endDate DATE, foodRequired INTEGER, woodRequired INTEGER, stoneRequired INTEGER, soldiersRequired INTEGER);
--
-- Create model donationEvent
--
CREATE TABLE `GrowYourEmpire_donationEvent` ('id' BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY, eventId BIGINT NOT NULL, owner_id VARCHAR(150) NOT NULL, donatedFood INTEGER, donatedWood INTEGER, donatedStone INTEGER, donatedSoldiers INTEGER);
--
-- Create constraint Test_testName on model test
--
ALTER TABLE `GrowYourEmpire_test` ADD CONSTRAINT `Test_testName` UNIQUE (`testName`);
--
-- Create constraint Question_questionText_testName on model question
--
ALTER TABLE `GrowYourEmpire_question` ADD CONSTRAINT `Question_questionText_testName` UNIQUE (`questionText`, `testName_id`);
--
-- Create constraint TestResolution_testName_studentName on model testresolution
--
ALTER TABLE `GrowYourEmpire_testresolution` ADD CONSTRAINT `TestResolution_testName_studentName` UNIQUE (`testName_id`, `studentName_id`);
--
-- Create constraint Upgrade_village_registeredDateTime on model upgrade
--
ALTER TABLE `GrowYourEmpire_upgrade` ADD CONSTRAINT `Upgrade_village_registeredDateTime` UNIQUE (`village_id`, `registeredDateTime`);
--
-- Create constraint Training_village_registeredDateTime on model training
--
ALTER TABLE `GrowYourEmpire_training` ADD CONSTRAINT `Training_village_registeredDateTime` UNIQUE (`village_id`, `registeredDateTime`);
--
-- Create constraint TradeOffer_source_destination_registeredDateTime on model tradeoffer
--
ALTER TABLE `GrowYourEmpire_tradeoffer` ADD CONSTRAINT `TradeOffer_source_destination_registeredDateTime` UNIQUE (`source_id`, `destination_id`, `registeredDateTime`);
--
-- Create constraint Bonus_village_registeredDateTime on model bonus
--
ALTER TABLE `GrowYourEmpire_bonus` ADD CONSTRAINT `Bonus_village_registeredDateTime` UNIQUE (`village_id`, `registeredDateTime`);
--
-- Create constraint Attack_attacker_defendant_registeredDateTime on model attack
--
ALTER TABLE `GrowYourEmpire_attack` ADD CONSTRAINT `Attack_attacker_defendant_registeredDateTime` UNIQUE (`attacker_id`, `defendant_id`, `registeredDateTime`);

ALTER TABLE `GrowYourEmpire_activity` ADD CONSTRAINT `Activity_date_owner_activityText` UNIQUE (`activityDate`, `owner_id`, `activityText`);
ALTER TABLE `GrowYourEmpire_student` ADD CONSTRAINT `GrowYourEmpire_student_user_id_ede2c4fc_fk_auth_user_username` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`username`);
ALTER TABLE `GrowYourEmpire_village` ADD CONSTRAINT `GrowYourEmpire_village_owner_id_6499c7d7_fk_DAWActivi` FOREIGN KEY (`owner_id`) REFERENCES `GrowYourEmpire_student` (`user_id`);
ALTER TABLE `GrowYourEmpire_student_subject` ADD CONSTRAINT `GrowYourEmpire_student_subject_student_id_subject_id_d6b1655e_uniq` UNIQUE (`student_id`, `subject_id`);
ALTER TABLE `GrowYourEmpire_student_subject` ADD CONSTRAINT `GrowYourEmpire_student__student_id_f4867e56_fk_DAWActivi` FOREIGN KEY (`student_id`) REFERENCES `GrowYourEmpire_student` (`user_id`);
ALTER TABLE `GrowYourEmpire_student_subject` ADD CONSTRAINT `GrowYourEmpire_student__subject_id_92cb0e07_fk_DAWActivi` FOREIGN KEY (`subject_id`) REFERENCES `GrowYourEmpire_subject` (`subjectName`);
ALTER TABLE `GrowYourEmpire_test` ADD CONSTRAINT `GrowYourEmpire_test_subject_id_59fa4403_fk_DAWActivi` FOREIGN KEY (`subject_id`) REFERENCES `GrowYourEmpire_subject` (`subjectName`);
ALTER TABLE `GrowYourEmpire_question` ADD CONSTRAINT `GrowYourEmpire_question_testName_id_41568988_fk_DAWActivi` FOREIGN KEY (`testName_id`) REFERENCES `GrowYourEmpire_test` (`testName`);
ALTER TABLE `GrowYourEmpire_testresolution` ADD CONSTRAINT `GrowYourEmpire_testreso_studentName_id_aad614cd_fk_DAWActivi` FOREIGN KEY (`studentName_id`) REFERENCES `GrowYourEmpire_student` (`user_id`);
ALTER TABLE `GrowYourEmpire_testresolution` ADD CONSTRAINT `GrowYourEmpire_testreso_testName_id_05f09d8c_fk_DAWActivi` FOREIGN KEY (`testName_id`) REFERENCES `GrowYourEmpire_test` (`testName`);
ALTER TABLE `GrowYourEmpire_option` ADD CONSTRAINT `GrowYourEmpire_option_questionText_id_62f3b8ec_fk_DAWActivi` FOREIGN KEY (`questionText_id`) REFERENCES `GrowYourEmpire_question` (`id`);
ALTER TABLE `GrowYourEmpire_upgrade` ADD CONSTRAINT `GrowYourEmpire_upgrade_village_id_408dce79_fk_DAWActivi` FOREIGN KEY (`village_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
ALTER TABLE `GrowYourEmpire_training` ADD CONSTRAINT `GrowYourEmpire_training_village_id_12790a97_fk_DAWActivi` FOREIGN KEY (`village_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
ALTER TABLE `GrowYourEmpire_tradeoffer` ADD CONSTRAINT `GrowYourEmpire_tradeoff_destination_id_2fd74c8a_fk_DAWActivi` FOREIGN KEY (`destination_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
ALTER TABLE `GrowYourEmpire_tradeoffer` ADD CONSTRAINT `GrowYourEmpire_tradeoff_source_id_34c879b6_fk_DAWActivi` FOREIGN KEY (`source_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
ALTER TABLE `GrowYourEmpire_bonus` ADD CONSTRAINT `GrowYourEmpire_bonus_village_id_8b96b70f_fk_DAWActivi` FOREIGN KEY (`village_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
ALTER TABLE `GrowYourEmpire_attack` ADD CONSTRAINT `GrowYourEmpire_attack_attacker_id_c3b71c8c_fk_DAWActivi` FOREIGN KEY (`attacker_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
ALTER TABLE `GrowYourEmpire_attack` ADD CONSTRAINT `GrowYourEmpire_attack_defendant_id_00414ff1_fk_DAWActivi` FOREIGN KEY (`defendant_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
ALTER TABLE `GrowYourEmpire_activity` ADD CONSTRAINT `GrowYourEmpire_activity_owner_id_909668dc_fk_DAWActivi` FOREIGN KEY (`owner_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
--
-- Create model God
--
CREATE TABLE `GrowYourEmpire_god` (`name` varchar(100) NOT NULL PRIMARY KEY, `desc` varchar(2000) NOT NULL, `bonus` varchar(200) NOT NULL);
--
-- Create model Subject
--
CREATE TABLE `GrowYourEmpire_subject` (`subjectName` varchar(100) NOT NULL PRIMARY KEY);
--
-- Create model Event
--
CREATE TABLE `GrowYourEmpire_event` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` varchar(100) NOT NULL, `desc` varchar(2000) NOT NULL, `startDate` datetime(6) NOT NULL, `endDate` datetime(6) NOT NULL, `foodRequired` integer NOT NULL, `woodRequired` integer NOT NULL, `stoneRequired` integer NOT NULL, `soldiersRequired` integer NOT NULL, CONSTRAINT `Event_title_startDate_endDate` UNIQUE (`title`, `startDate`, `endDate`));
--
-- Create model New
--
CREATE TABLE `GrowYourEmpire_new` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` varchar(100) NOT NULL, `desc` varchar(2000) NOT NULL, `registeredDateTime` datetime(6) NOT NULL, CONSTRAINT `New_title_registeredDateTime` UNIQUE (`title`, `registeredDateTime`));
--
-- Create model Student
--
CREATE TABLE `GrowYourEmpire_student` (`user_id` varchar(150) NOT NULL PRIMARY KEY);
CREATE TABLE `GrowYourEmpire_student_subject` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `student_id` varchar(150) NOT NULL, `subject_id` varchar(100) NOT NULL);
--
-- Create model Test
--
CREATE TABLE `GrowYourEmpire_test` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `testName` varchar(50) NOT NULL, `date` datetime(6) NOT NULL, `subject_id` varchar(100) NOT NULL);
--
-- Create model Question
--
CREATE TABLE `GrowYourEmpire_question` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `questionText` varchar(50) NOT NULL, `expectedText` varchar(100) NOT NULL, `questionType` varchar(50) NOT NULL, `testName_id` varchar(50) NOT NULL);
--
-- Create model TestResolution
--
CREATE TABLE `GrowYourEmpire_testresolution` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `points` integer NOT NULL, `studentName_id` varchar(150) NOT NULL, `testName_id` varchar(50) NOT NULL);
--
-- Create model Option
--
CREATE TABLE `GrowYourEmpire_option` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `questionOptionText` varchar(50) NOT NULL, `correctOption` bool NOT NULL, `questionText_id` bigint NOT NULL, CONSTRAINT `Option_questionText_questionOptionText` UNIQUE (`questionOptionText`, `questionText_id`));
--
-- Create model Village
--
CREATE TABLE `GrowYourEmpire_village` (`villageName` varchar(50) NOT NULL, `dailyFood` integer NOT NULL, `dailyWood` integer NOT NULL, `dailyStone` integer NOT NULL, `storedFood` integer NOT NULL, `storedWood` integer NOT NULL, `storedStone` integer NOT NULL, `foodLevel` integer NOT NULL, `woodLevel` integer NOT NULL, `stoneLevel` integer NOT NULL, `wallLevel` integer NOT NULL, `storageLevel` integer NOT NULL, `soldiers` integer NOT NULL, `lastLogin` date NOT NULL, `disabled` bool NOT NULL, `owner_id` varchar(150) NOT NULL PRIMARY KEY, `god_id` varchar(100) NULL);
--
-- Create model Upgrade
--
CREATE TABLE `GrowYourEmpire_upgrade` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `registeredDateTime` datetime(6) NOT NULL, `level` integer NOT NULL, `building` integer NOT NULL, `woodCost` integer NOT NULL, `stoneCost` integer NOT NULL, `completed` bool NOT NULL, `village_id` varchar(150) NOT NULL);
--
-- Create model Training
--
CREATE TABLE `GrowYourEmpire_training` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `registeredDateTime` datetime(6) NOT NULL, `units` integer NOT NULL, `foodCost` integer NOT NULL, `completed` bool NOT NULL, `village_id` varchar(150) NOT NULL);
--
-- Create model TradeOffer
--
CREATE TABLE `GrowYourEmpire_tradeoffer` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `registeredDateTime` datetime(6) NOT NULL, `wantedWood` integer NOT NULL, `wantedFood` integer NOT NULL, `wantedStone` integer NOT NULL, `offeredWood` integer NOT NULL, `offeredFood` integer NOT NULL, `offeredStone` integer NOT NULL, `accepted` bool NOT NULL, `destination_id` varchar(150) NOT NULL, `source_id` varchar(150) NOT NULL);
--
-- Create model DonationEvent
--
CREATE TABLE `GrowYourEmpire_donationevent` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `donatedFood` integer NOT NULL, `donatedWood` integer NOT NULL, `donatedStone` integer NOT NULL, `donatedSoldiers` integer NOT NULL, `event_id` bigint NOT NULL, `owner_id` varchar(150) NOT NULL);
--
-- Create model Bonus
--
CREATE TABLE `GrowYourEmpire_bonus` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `registeredDateTime` datetime(6) NOT NULL, `bonusType` integer NOT NULL, `bonusAmount` integer NOT NULL, `completed` bool NOT NULL, `village_id` varchar(150) NOT NULL);
--
-- Create model Attack
--
CREATE TABLE `GrowYourEmpire_attack` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `usedSoldiers` integer NOT NULL, `registeredDateTime` datetime(6) NOT NULL, `completed` bool NOT NULL, `attacker_id` varchar(150) NOT NULL, `defendant_id` varchar(150) NOT NULL);
--
-- Create model Activity
--
CREATE TABLE `GrowYourEmpire_activity` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `activityText` varchar(150) NOT NULL, `activityDate` datetime(6) NOT NULL, `owner_id` varchar(150) NOT NULL);
--
-- Create constraint Test_testName on model test
--
ALTER TABLE `GrowYourEmpire_test` ADD CONSTRAINT `Test_testName` UNIQUE (`testName`);
--
-- Create constraint Question_questionText_testName on model question
--
ALTER TABLE `GrowYourEmpire_question` ADD CONSTRAINT `Question_questionText_testName` UNIQUE (`questionText`, `testName_id`);
--
-- Create constraint TestResolution_testName_studentName on model testresolution
--
ALTER TABLE `GrowYourEmpire_testresolution` ADD CONSTRAINT `TestResolution_testName_studentName` UNIQUE (`testName_id`, `studentName_id`);
--
-- Create constraint Upgrade_village_registeredDateTime on model upgrade
--
ALTER TABLE `GrowYourEmpire_upgrade` ADD CONSTRAINT `Upgrade_village_registeredDateTime` UNIQUE (`village_id`, `registeredDateTime`);
--
-- Create constraint Training_village_registeredDateTime on model training
--
ALTER TABLE `GrowYourEmpire_training` ADD CONSTRAINT `Training_village_registeredDateTime` UNIQUE (`village_id`, `registeredDateTime`);
--
-- Create constraint TradeOffer_source_destination_registeredDateTime on model tradeoffer
--
ALTER TABLE `GrowYourEmpire_tradeoffer` ADD CONSTRAINT `TradeOffer_source_destination_registeredDateTime` UNIQUE (`source_id`, `destination_id`, `registeredDateTime`);
--
-- Create constraint Bonus_village_registeredDateTime on model bonus
--
ALTER TABLE `GrowYourEmpire_bonus` ADD CONSTRAINT `Bonus_village_registeredDateTime` UNIQUE (`village_id`, `registeredDateTime`);
--
-- Create constraint Attack_attacker_defendant_registeredDateTime on model attack
--
ALTER TABLE `GrowYourEmpire_attack` ADD CONSTRAINT `Attack_attacker_defendant_registeredDateTime` UNIQUE (`attacker_id`, `defendant_id`, `registeredDateTime`);
--
-- Create constraint Activity_date_owner_activityText on model activity
--
ALTER TABLE `GrowYourEmpire_activity` ADD CONSTRAINT `Activity_date_owner_activityText` UNIQUE (`activityDate`, `owner_id`, `activityText`);
ALTER TABLE `GrowYourEmpire_student` ADD CONSTRAINT `GrowYourEmpire_student_user_id_1c0876c6_fk_auth_user_username` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`username`);
ALTER TABLE `GrowYourEmpire_student_subject` ADD CONSTRAINT `GrowYourEmpire_student_s_student_id_subject_id_ed2e1598_uniq` UNIQUE (`student_id`, `subject_id`);
ALTER TABLE `GrowYourEmpire_student_subject` ADD CONSTRAINT `GrowYourEmpire_stude_student_id_28d4b686_fk_GrowYourE` FOREIGN KEY (`student_id`) REFERENCES `GrowYourEmpire_student` (`user_id`);
ALTER TABLE `GrowYourEmpire_student_subject` ADD CONSTRAINT `GrowYourEmpire_stude_subject_id_74a86a46_fk_GrowYourE` FOREIGN KEY (`subject_id`) REFERENCES `GrowYourEmpire_subject` (`subjectName`);
ALTER TABLE `GrowYourEmpire_test` ADD CONSTRAINT `GrowYourEmpire_test_subject_id_7cacf2de_fk_GrowYourE` FOREIGN KEY (`subject_id`) REFERENCES `GrowYourEmpire_subject` (`subjectName`);
ALTER TABLE `GrowYourEmpire_question` ADD CONSTRAINT `GrowYourEmpire_quest_testName_id_17e2caaa_fk_GrowYourE` FOREIGN KEY (`testName_id`) REFERENCES `GrowYourEmpire_test` (`testName`);
ALTER TABLE `GrowYourEmpire_testresolution` ADD CONSTRAINT `GrowYourEmpire_testr_studentName_id_662517be_fk_GrowYourE` FOREIGN KEY (`studentName_id`) REFERENCES `GrowYourEmpire_student` (`user_id`);
ALTER TABLE `GrowYourEmpire_testresolution` ADD CONSTRAINT `GrowYourEmpire_testr_testName_id_7c90439a_fk_GrowYourE` FOREIGN KEY (`testName_id`) REFERENCES `GrowYourEmpire_test` (`testName`);
ALTER TABLE `GrowYourEmpire_option` ADD CONSTRAINT `GrowYourEmpire_optio_questionText_id_ac1c71bb_fk_GrowYourE` FOREIGN KEY (`questionText_id`) REFERENCES `GrowYourEmpire_question` (`id`);
ALTER TABLE `GrowYourEmpire_village` ADD CONSTRAINT `GrowYourEmpire_villa_owner_id_a3d9ba8f_fk_GrowYourE` FOREIGN KEY (`owner_id`) REFERENCES `GrowYourEmpire_student` (`user_id`);
ALTER TABLE `GrowYourEmpire_village` ADD CONSTRAINT `GrowYourEmpire_villa_god_id_5301142c_fk_GrowYourE` FOREIGN KEY (`god_id`) REFERENCES `GrowYourEmpire_god` (`name`);
ALTER TABLE `GrowYourEmpire_upgrade` ADD CONSTRAINT `GrowYourEmpire_upgra_village_id_8a342f7e_fk_GrowYourE` FOREIGN KEY (`village_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
ALTER TABLE `GrowYourEmpire_training` ADD CONSTRAINT `GrowYourEmpire_train_village_id_08a98392_fk_GrowYourE` FOREIGN KEY (`village_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
ALTER TABLE `GrowYourEmpire_tradeoffer` ADD CONSTRAINT `GrowYourEmpire_trade_destination_id_83cddff9_fk_GrowYourE` FOREIGN KEY (`destination_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
ALTER TABLE `GrowYourEmpire_tradeoffer` ADD CONSTRAINT `GrowYourEmpire_trade_source_id_7cf53aa8_fk_GrowYourE` FOREIGN KEY (`source_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
ALTER TABLE `GrowYourEmpire_donationevent` ADD CONSTRAINT `GrowYourEmpire_donat_event_id_9a8887db_fk_GrowYourE` FOREIGN KEY (`event_id`) REFERENCES `GrowYourEmpire_event` (`id`);
ALTER TABLE `GrowYourEmpire_donationevent` ADD CONSTRAINT `GrowYourEmpire_donat_owner_id_794ff731_fk_GrowYourE` FOREIGN KEY (`owner_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
ALTER TABLE `GrowYourEmpire_bonus` ADD CONSTRAINT `GrowYourEmpire_bonus_village_id_12d619ba_fk_GrowYourE` FOREIGN KEY (`village_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
ALTER TABLE `GrowYourEmpire_attack` ADD CONSTRAINT `GrowYourEmpire_attac_attacker_id_44694344_fk_GrowYourE` FOREIGN KEY (`attacker_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
ALTER TABLE `GrowYourEmpire_attack` ADD CONSTRAINT `GrowYourEmpire_attac_defendant_id_4cd77641_fk_GrowYourE` FOREIGN KEY (`defendant_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
ALTER TABLE `GrowYourEmpire_activity` ADD CONSTRAINT `GrowYourEmpire_activ_owner_id_ee12241b_fk_GrowYourE` FOREIGN KEY (`owner_id`) REFERENCES `GrowYourEmpire_village` (`owner_id`);
