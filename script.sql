--
-- Create model Student
--
CREATE TABLE `DAWActivity_student` (`user_id` varchar(150) NOT NULL PRIMARY KEY);
--
-- Create model Subject
--
CREATE TABLE `DAWActivity_subject` (`subjectName` varchar(100) NOT NULL PRIMARY KEY);
--
-- Create model New
--
CREATE TABLE `DAWActivity_new` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` varchar(100) NOT NULL, `desc` varchar(2000) NOT NULL, `registeredDateTime` datetime(6) NOT NULL, CONSTRAINT `New_title_registeredDateTime` UNIQUE (`title`, `registeredDateTime`));
--
-- Create model Village
--
CREATE TABLE `DAWActivity_village` (`villageName` varchar(50) NOT NULL, `dailyFood` integer NOT NULL, `dailyWood` integer NOT NULL, `dailyStone` integer NOT NULL, `storedFood` integer NOT NULL, `storedWood` integer NOT NULL, `storedStone` integer NOT NULL, `foodLevel` integer NOT NULL, `woodLevel` integer NOT NULL, `stoneLevel` integer NOT NULL, `wallLevel` integer NOT NULL, `storageLevel` integer NOT NULL, `soldiers` integer NOT NULL, `lastLogin` date NOT NULL, `disabled` bool NOT NULL, `owner_id` varchar(150) NOT NULL PRIMARY KEY);
--
-- Add field subject to student
--
CREATE TABLE `DAWActivity_student_subject` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `student_id` varchar(150) NOT NULL, `subject_id` varchar(100) NOT NULL);
--
-- Create model Test
--
CREATE TABLE `DAWActivity_test` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `testName` varchar(50) NOT NULL, `date` datetime(6) NOT NULL, `subject_id` varchar(100) NOT NULL);
--
-- Create model Question
--
CREATE TABLE `DAWActivity_question` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `questionText` varchar(50) NOT NULL, `expectedText` varchar(100) NOT NULL, `questionType` varchar(50) NOT NULL, `testName_id` varchar(50) NOT NULL);
--
-- Create model TestResolution
--
CREATE TABLE `DAWActivity_testresolution` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `points` integer NOT NULL, `studentName_id` varchar(150) NOT NULL, `testName_id` varchar(50) NOT NULL);
--
-- Create model Option
--
CREATE TABLE `DAWActivity_option` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `questionOptionText` varchar(50) NOT NULL, `correctOption` bool NOT NULL, `questionText_id` bigint NOT NULL, CONSTRAINT `Option_questionText_questionOptionText` UNIQUE (`questionOptionText`, `questionText_id`));
--
-- Create model Upgrade
--
CREATE TABLE `DAWActivity_upgrade` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `registeredDateTime` datetime(6) NOT NULL, `level` integer NOT NULL, `building` integer NOT NULL, `woodCost` integer NOT NULL, `stoneCost` integer NOT NULL, `completed` bool NOT NULL, `village_id` varchar(150) NOT NULL);
--
-- Create model Training
--
CREATE TABLE `DAWActivity_training` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `registeredDateTime` datetime(6) NOT NULL, `units` integer NOT NULL, `foodCost` integer NOT NULL, `completed` bool NOT NULL, `village_id` varchar(150) NOT NULL);
--
-- Create model TradeOffer
--
CREATE TABLE `DAWActivity_tradeoffer` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `registeredDateTime` datetime(6) NOT NULL, `wantedWood` integer NOT NULL, `wantedFood` integer NOT NULL, `wantedStone` integer NOT NULL, `offeredWood` integer NOT NULL, `offeredFood` integer NOT NULL, `offeredStone` integer NOT NULL, `accepted` bool NOT NULL, `destination_id` varchar(150) NOT NULL, `source_id` varchar(150) NOT NULL);
--
-- Create model Bonus
--
CREATE TABLE `DAWActivity_bonus` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `registeredDateTime` datetime(6) NOT NULL, `bonusType` integer NOT NULL, `bonusAmount` integer NOT NULL, `completed` bool NOT NULL, `village_id` varchar(150) NOT NULL);
--
-- Create model Attack
--
CREATE TABLE `DAWActivity_attack` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `usedSoldiers` integer NOT NULL, `registeredDateTime` datetime(6) NOT NULL, `completed` bool NOT NULL, `attacker_id` varchar(150) NOT NULL, `defendant_id` varchar(150) NOT NULL);
--
-- Create model Activity
--
CREATE TABLE `DAWActivity_activity` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `activityText` varchar(150) NOT NULL, `activityDate` datetime(6) NOT NULL, `owner_id` varchar(150) NOT NULL);
--
-- Create constraint Test_testName on model test
--
ALTER TABLE `DAWActivity_test` ADD CONSTRAINT `Test_testName` UNIQUE (`testName`);
--
-- Create constraint Question_questionText_testName on model question
--
ALTER TABLE `DAWActivity_question` ADD CONSTRAINT `Question_questionText_testName` UNIQUE (`questionText`, `testName_id`);
--
-- Create constraint TestResolution_testName_studentName on model testresolution
--
ALTER TABLE `DAWActivity_testresolution` ADD CONSTRAINT `TestResolution_testName_studentName` UNIQUE (`testName_id`, `studentName_id`);
--
-- Create constraint Upgrade_village_registeredDateTime on model upgrade
--
ALTER TABLE `DAWActivity_upgrade` ADD CONSTRAINT `Upgrade_village_registeredDateTime` UNIQUE (`village_id`, `registeredDateTime`);
--
-- Create constraint Training_village_registeredDateTime on model training
--
ALTER TABLE `DAWActivity_training` ADD CONSTRAINT `Training_village_registeredDateTime` UNIQUE (`village_id`, `registeredDateTime`);
--
-- Create constraint TradeOffer_source_destination_registeredDateTime on model tradeoffer
--
ALTER TABLE `DAWActivity_tradeoffer` ADD CONSTRAINT `TradeOffer_source_destination_registeredDateTime` UNIQUE (`source_id`, `destination_id`, `registeredDateTime`);
--
-- Create constraint Bonus_village_registeredDateTime on model bonus
--
ALTER TABLE `DAWActivity_bonus` ADD CONSTRAINT `Bonus_village_registeredDateTime` UNIQUE (`village_id`, `registeredDateTime`);
--
-- Create constraint Attack_attacker_defendant_registeredDateTime on model attack
--
ALTER TABLE `DAWActivity_attack` ADD CONSTRAINT `Attack_attacker_defendant_registeredDateTime` UNIQUE (`attacker_id`, `defendant_id`, `registeredDateTime`);
--
-- Create constraint Activity_date_owner_activityText on model activity
--
ALTER TABLE `DAWActivity_activity` ADD CONSTRAINT `Activity_date_owner_activityText` UNIQUE (`activityDate`, `owner_id`, `activityText`);
ALTER TABLE `DAWActivity_student` ADD CONSTRAINT `DAWActivity_student_user_id_ede2c4fc_fk_auth_user_username` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`username`);
ALTER TABLE `DAWActivity_village` ADD CONSTRAINT `DAWActivity_village_owner_id_6499c7d7_fk_DAWActivi` FOREIGN KEY (`owner_id`) REFERENCES `DAWActivity_student` (`user_id`);
ALTER TABLE `DAWActivity_student_subject` ADD CONSTRAINT `DAWActivity_student_subject_student_id_subject_id_d6b1655e_uniq` UNIQUE (`student_id`, `subject_id`);
ALTER TABLE `DAWActivity_student_subject` ADD CONSTRAINT `DAWActivity_student__student_id_f4867e56_fk_DAWActivi` FOREIGN KEY (`student_id`) REFERENCES `DAWActivity_student` (`user_id`);
ALTER TABLE `DAWActivity_student_subject` ADD CONSTRAINT `DAWActivity_student__subject_id_92cb0e07_fk_DAWActivi` FOREIGN KEY (`subject_id`) REFERENCES `DAWActivity_subject` (`subjectName`);
ALTER TABLE `DAWActivity_test` ADD CONSTRAINT `DAWActivity_test_subject_id_59fa4403_fk_DAWActivi` FOREIGN KEY (`subject_id`) REFERENCES `DAWActivity_subject` (`subjectName`);
ALTER TABLE `DAWActivity_question` ADD CONSTRAINT `DAWActivity_question_testName_id_41568988_fk_DAWActivi` FOREIGN KEY (`testName_id`) REFERENCES `DAWActivity_test` (`testName`);
ALTER TABLE `DAWActivity_testresolution` ADD CONSTRAINT `DAWActivity_testreso_studentName_id_aad614cd_fk_DAWActivi` FOREIGN KEY (`studentName_id`) REFERENCES `DAWActivity_student` (`user_id`);
ALTER TABLE `DAWActivity_testresolution` ADD CONSTRAINT `DAWActivity_testreso_testName_id_05f09d8c_fk_DAWActivi` FOREIGN KEY (`testName_id`) REFERENCES `DAWActivity_test` (`testName`);
ALTER TABLE `DAWActivity_option` ADD CONSTRAINT `DAWActivity_option_questionText_id_62f3b8ec_fk_DAWActivi` FOREIGN KEY (`questionText_id`) REFERENCES `DAWActivity_question` (`id`);
ALTER TABLE `DAWActivity_upgrade` ADD CONSTRAINT `DAWActivity_upgrade_village_id_408dce79_fk_DAWActivi` FOREIGN KEY (`village_id`) REFERENCES `DAWActivity_village` (`owner_id`);
ALTER TABLE `DAWActivity_training` ADD CONSTRAINT `DAWActivity_training_village_id_12790a97_fk_DAWActivi` FOREIGN KEY (`village_id`) REFERENCES `DAWActivity_village` (`owner_id`);
ALTER TABLE `DAWActivity_tradeoffer` ADD CONSTRAINT `DAWActivity_tradeoff_destination_id_2fd74c8a_fk_DAWActivi` FOREIGN KEY (`destination_id`) REFERENCES `DAWActivity_village` (`owner_id`);
ALTER TABLE `DAWActivity_tradeoffer` ADD CONSTRAINT `DAWActivity_tradeoff_source_id_34c879b6_fk_DAWActivi` FOREIGN KEY (`source_id`) REFERENCES `DAWActivity_village` (`owner_id`);
ALTER TABLE `DAWActivity_bonus` ADD CONSTRAINT `DAWActivity_bonus_village_id_8b96b70f_fk_DAWActivi` FOREIGN KEY (`village_id`) REFERENCES `DAWActivity_village` (`owner_id`);
ALTER TABLE `DAWActivity_attack` ADD CONSTRAINT `DAWActivity_attack_attacker_id_c3b71c8c_fk_DAWActivi` FOREIGN KEY (`attacker_id`) REFERENCES `DAWActivity_village` (`owner_id`);
ALTER TABLE `DAWActivity_attack` ADD CONSTRAINT `DAWActivity_attack_defendant_id_00414ff1_fk_DAWActivi` FOREIGN KEY (`defendant_id`) REFERENCES `DAWActivity_village` (`owner_id`);
ALTER TABLE `DAWActivity_activity` ADD CONSTRAINT `DAWActivity_activity_owner_id_909668dc_fk_DAWActivi` FOREIGN KEY (`owner_id`) REFERENCES `DAWActivity_village` (`owner_id`);
