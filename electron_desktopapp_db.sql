-- phpMyAdmin SQL Dump
-- version 5.2.1deb3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 23, 2026 at 03:59 PM
-- Server version: 8.0.45-0ubuntu0.24.04.1
-- PHP Version: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `electron_desktopapp_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `licenses`
--

CREATE TABLE `licenses` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `license_key` varchar(120) DEFAULT NULL,
  `plan_key` varchar(20) DEFAULT NULL,
  `plan_id` int DEFAULT NULL,
  `plan_name` varchar(50) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `days` int DEFAULT NULL,
  `products_limit` varchar(20) DEFAULT NULL,
  `bills_limit` varchar(20) DEFAULT NULL,
  `users_limit` int DEFAULT NULL,
  `support_type` varchar(20) DEFAULT NULL,
  `active_user` int DEFAULT '0',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `licenses`
--

INSERT INTO `licenses` (`id`, `user_id`, `license_key`, `plan_key`, `plan_id`, `plan_name`, `price`, `start_date`, `expiry_date`, `days`, `products_limit`, `bills_limit`, `users_limit`, `support_type`, `active_user`, `status`, `created_at`) VALUES
(1, 1, 'LIC-3B91923B38DB00AC', 'monthly', 2, 'Monthly', 2.00, '2026-03-07', '2026-04-06', 30, '2', '5', 7, 'Email', 4, '1', '2026-03-07 17:30:31'),
(2, 1, 'LIC-EEDBF1510370922E', 'trial', 1, 'Trial', 0.00, '2026-03-07', '2026-03-08', 1, '2', '3', 1, 'Basic', 0, '0', '2026-03-07 17:32:26'),
(3, 1, 'LIC-286CC5C2FCF9A580', 'monthly', 2, 'Monthly', 2.00, '2026-03-08', '2026-03-20', 30, '3', '5', 2, 'Email', 1, '1', '2026-03-09 12:43:35'),
(4, 2, 'LIC-11AFD0CF4DCD8B0C', 'trial', 1, 'Trial', 0.00, '2026-03-09', '2026-03-10', 1, '2', '3', 1, 'Basic', 0, '1', '2026-03-09 17:42:54'),
(5, 1, 'LIC-1889A539DEF4586B', 'monthly', 2, 'Monthly', 2.00, '2026-03-17', '2026-04-16', 30, '100', '500', 2, 'Email', 2, '1', '2026-03-17 11:21:13'),
(6, 3, 'LIC-FF9EEC7DE6EE91A2', 'trial', 1, 'Trial', 0.00, '2026-03-17', '2026-03-20', 1, '10', '500', 5, 'Basic', 3, '0', '2026-03-17 11:25:08'),
(7, 4, 'LIC-C84B430D23CB861F', 'trial', 1, 'Trial', 0.00, '2026-03-17', '2026-03-18', 1, '2', '3', 1, 'Basic', 1, '1', '2026-03-17 15:08:52');

-- --------------------------------------------------------

--
-- Table structure for table `master_customers`
--

CREATE TABLE `master_customers` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `shop_name` varchar(150) DEFAULT NULL,
  `email` varchar(150) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `address` text,
  `password` varchar(200) NOT NULL,
  `status` tinyint DEFAULT '1' COMMENT '1=active,0=inactive',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `master_customers`
--

INSERT INTO `master_customers` (`id`, `name`, `shop_name`, `email`, `mobile`, `address`, `password`, `status`, `created_at`, `updated_at`) VALUES
(1, 'Aakash Dhandode', 'synques', 'aakash.dhandode@synques.in', '8085316017', 'bhopal', '123', 1, '2026-03-07 17:27:03', '2026-03-09 12:39:02'),
(2, 'Aakash Dhandode', 'synques', 'aakashdha2099@gmail.com', '8085316017', 'bhopal', '123', 1, '2026-03-09 17:40:13', '2026-03-17 11:23:35'),
(3, 'Aakash Dhandode', 'bake n sheke', 'aakashdha2019@gmail.com', '8085316017', 'bhopal', '123', 1, '2026-03-17 11:24:18', '2026-03-17 11:24:18'),
(4, 'Mayank Jain SynQues', 'SynQues Consultancy Pvt Ltd', 'mayank.jain@synques.in', '09752971303', '289, Jain Nagar,\r\nNa=ear Gufam Mandir Road, Lalghati', 'synques12345', 1, '2026-03-17 15:07:28', '2026-03-17 15:07:28');

-- --------------------------------------------------------

--
-- Table structure for table `master_payments`
--

CREATE TABLE `master_payments` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `license_id` int DEFAULT NULL,
  `gateway` varchar(50) DEFAULT 'RAZORPAY',
  `order_id` varchar(150) NOT NULL,
  `payment_id` varchar(150) DEFAULT NULL,
  `razorpay_signature` varchar(255) DEFAULT NULL,
  `txn_id` varchar(150) DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `currency` varchar(10) DEFAULT 'INR',
  `payment_method` varchar(50) DEFAULT NULL,
  `payment_status` tinyint DEFAULT '1' COMMENT '1=pending,2=success,3=failed',
  `payment_request` json DEFAULT NULL,
  `payment_response` json DEFAULT NULL,
  `customer_name` varchar(100) DEFAULT NULL,
  `customer_email` varchar(100) DEFAULT NULL,
  `customer_mobile` varchar(20) DEFAULT NULL,
  `customer_address` text,
  `paid_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `master_payments`
--

INSERT INTO `master_payments` (`id`, `user_id`, `license_id`, `gateway`, `order_id`, `payment_id`, `razorpay_signature`, `txn_id`, `amount`, `currency`, `payment_method`, `payment_status`, `payment_request`, `payment_response`, `customer_name`, `customer_email`, `customer_mobile`, `customer_address`, `paid_at`, `created_at`, `updated_at`) VALUES
(1, 1, NULL, 'RAZORPAY', 'order_SOKMkHY8wroPMZ', NULL, NULL, NULL, 2.00, 'INR', 'RAZORPAY', 1, '{\"name\": \"Aakash Dhandode\", \"plan\": \"monthly\", \"shop\": \"synques\", \"email\": \"aakash.dhandode@synques.in\", \"mobile\": \"8085316017\", \"address\": \"bhopal\"}', '{\"id\": \"order_SOKMkHY8wroPMZ\", \"notes\": [], \"amount\": 200, \"entity\": \"order\", \"status\": \"created\", \"receipt\": \"rcpt_1772884709\", \"attempts\": 0, \"currency\": \"INR\", \"offer_id\": null, \"amount_due\": 200, \"created_at\": 1772884710, \"amount_paid\": 0}', 'Aakash Dhandode', 'aakash.dhandode@synques.in', '8085316017', 'bhopal', NULL, '2026-03-07 17:28:30', '2026-03-07 17:28:30'),
(2, 1, NULL, 'RAZORPAY', 'order_SOKNofLQ6IN9Rb', NULL, NULL, NULL, 2.00, 'INR', 'RAZORPAY', 1, '{\"name\": \"Aakash Dhandode\", \"plan\": \"monthly\", \"shop\": \"synques\", \"email\": \"aakash.dhandode@synques.in\", \"mobile\": \"8085316017\", \"address\": \"bhopal\"}', '{\"id\": \"order_SOKNofLQ6IN9Rb\", \"notes\": [], \"amount\": 200, \"entity\": \"order\", \"status\": \"created\", \"receipt\": \"rcpt_1772884770\", \"attempts\": 0, \"currency\": \"INR\", \"offer_id\": null, \"amount_due\": 200, \"created_at\": 1772884770, \"amount_paid\": 0}', 'Aakash Dhandode', 'aakash.dhandode@synques.in', '8085316017', 'bhopal', NULL, '2026-03-07 17:29:30', '2026-03-07 17:43:16'),
(3, 1, 1, 'RAZORPAY', 'order_SOKONNJ7oJY50n', 'pay_SOKOZdUE18kASn', '3384455ca5a02b3f136478a77744a01f3124474be6d051fb9ec803493507edfd', 'pay_SOKOZdUE18kASn', 2.00, 'INR', 'RAZORPAY', 2, '{\"name\": \"Aakash Dhandode\", \"plan\": \"monthly\", \"shop\": \"synques\", \"email\": \"aakash.dhandode@synques.in\", \"mobile\": \"8085316017\", \"address\": \"bhopal\"}', '{\"order_id\": \"order_SOKONNJ7oJY50n\", \"signature\": \"3384455ca5a02b3f136478a77744a01f3124474be6d051fb9ec803493507edfd\", \"payment_id\": \"pay_SOKOZdUE18kASn\"}', 'Aakash Dhandode', 'aakash.dhandode@synques.in', '8085316017', 'bhopal', '2026-03-07 17:30:31', '2026-03-07 17:30:02', '2026-03-07 17:30:31'),
(4, 1, 2, 'TRIAL', 'TRIAL_1772884946', 'TRIALPAY_1772884946', 'TRIAL', '0', 0.00, 'INR', 'TRIAL', 2, '{\"name\": \"Aakash Dhandode\", \"plan\": \"trial\", \"shop\": \"synques\", \"email\": \"aakash.dhandode@synques.in\", \"mobile\": \"8085316017\", \"address\": \"bhopal\"}', '{\"type\": \"TRIAL\"}', 'Aakash Dhandode', 'aakash.dhandode@synques.in', '8085316017', 'bhopal', '2026-03-07 17:32:26', '2026-03-07 17:32:26', '2026-03-07 17:32:26'),
(5, 1, 3, 'RAZORPAY', 'order_SP2ZZPZPLIucDI', 'pay_SP2Zi75HGTZRl9', '1f5c552b24bb4295ea64b4c4ceaa00772a2531703d08be3560b8ce30565e3811', 'pay_SP2Zi75HGTZRl9', 2.00, 'INR', 'RAZORPAY', 2, '{\"name\": \"Aakash Dhandode\", \"plan\": \"monthly\", \"shop\": \"synques\", \"email\": \"aakash.dhandode@synques.in\", \"mobile\": \"8085316017\", \"address\": \"bhopal\"}', '{\"order_id\": \"order_SP2ZZPZPLIucDI\", \"signature\": \"1f5c552b24bb4295ea64b4c4ceaa00772a2531703d08be3560b8ce30565e3811\", \"payment_id\": \"pay_SP2Zi75HGTZRl9\"}', 'Aakash Dhandode', 'aakash.dhandode@synques.in', '8085316017', 'bhopal', '2026-03-09 12:43:35', '2026-03-09 12:43:09', '2026-03-09 12:43:35'),
(6, 2, 4, 'TRIAL', 'TRIAL_1773058374', 'TRIALPAY_1773058374', 'TRIAL', '0', 0.00, 'INR', 'TRIAL', 2, '{\"name\": \"Aakash Dhandode\", \"plan\": \"trial\", \"shop\": \"synques\", \"email\": \"aakashdha2019@gmail.com\", \"mobile\": \"8085316017\", \"address\": \"bhopal\"}', '{\"type\": \"TRIAL\"}', 'Aakash Dhandode', 'aakashdha2019@gmail.com', '8085316017', 'bhopal', '2026-03-09 17:42:54', '2026-03-09 17:42:54', '2026-03-09 17:42:54'),
(7, 1, NULL, 'RAZORPAY', 'order_SSBQKvcSLw688h', NULL, NULL, NULL, 2.00, 'INR', 'RAZORPAY', 1, '{\"name\": \"Aakash Dhandode\", \"plan\": \"monthly\", \"shop\": \"synques\", \"email\": \"aakash.dhandode@synques.in\", \"mobile\": \"8085316017\", \"address\": \"bhopal\"}', '{\"id\": \"order_SSBQKvcSLw688h\", \"notes\": [], \"amount\": 200, \"entity\": \"order\", \"status\": \"created\", \"receipt\": \"rcpt_1773726579\", \"attempts\": 0, \"currency\": \"INR\", \"offer_id\": null, \"amount_due\": 200, \"created_at\": 1773726579, \"amount_paid\": 0}', 'Aakash Dhandode', 'aakash.dhandode@synques.in', '8085316017', 'bhopal', NULL, '2026-03-17 11:19:40', '2026-03-17 11:19:40'),
(8, 1, 5, 'RAZORPAY', 'order_SSBRd15P14uwri', 'pay_SSBRhOOMFg1vxK', '0e4d50086f3791c62875fb4fe335fcd6bd44851844f850c764af09c84a899696', 'pay_SSBRhOOMFg1vxK', 2.00, 'INR', 'RAZORPAY', 2, '{\"name\": \"Aakash Dhandode\", \"plan\": \"monthly\", \"shop\": \"synques\", \"email\": \"aakash.dhandode@synques.in\", \"mobile\": \"8085316017\", \"address\": \"bhopal\"}', '{\"order_id\": \"order_SSBRd15P14uwri\", \"signature\": \"0e4d50086f3791c62875fb4fe335fcd6bd44851844f850c764af09c84a899696\", \"payment_id\": \"pay_SSBRhOOMFg1vxK\"}', 'Aakash Dhandode', 'aakash.dhandode@synques.in', '8085316017', 'bhopal', '2026-03-17 11:21:13', '2026-03-17 11:20:53', '2026-03-17 11:21:13'),
(9, 3, NULL, 'RAZORPAY', 'order_SSBVrdgVmMRtiT', NULL, NULL, NULL, 2.00, 'INR', 'RAZORPAY', 1, '{\"name\": \"Aakash Dhandode\", \"plan\": \"monthly\", \"shop\": \"bake n sheke\", \"email\": \"aakashdha2019@gmail.com\", \"mobile\": \"8085316017\", \"address\": \"bhopal\"}', '{\"id\": \"order_SSBVrdgVmMRtiT\", \"notes\": [], \"amount\": 200, \"entity\": \"order\", \"status\": \"created\", \"receipt\": \"rcpt_1773726893\", \"attempts\": 0, \"currency\": \"INR\", \"offer_id\": null, \"amount_due\": 200, \"created_at\": 1773726893, \"amount_paid\": 0}', 'Aakash Dhandode', 'aakashdha2019@gmail.com', '8085316017', 'bhopal', NULL, '2026-03-17 11:24:53', '2026-03-17 11:24:53'),
(10, 3, 6, 'TRIAL', 'TRIAL_1773726908', 'TRIALPAY_1773726908', 'TRIAL', '0', 0.00, 'INR', 'TRIAL', 2, '{\"name\": \"Aakash Dhandode\", \"plan\": \"trial\", \"shop\": \"bake n sheke\", \"email\": \"aakashdha2019@gmail.com\", \"mobile\": \"8085316017\", \"address\": \"bhopal\"}', '{\"type\": \"TRIAL\"}', 'Aakash Dhandode', 'aakashdha2019@gmail.com', '8085316017', 'bhopal', '2026-03-17 11:25:08', '2026-03-17 11:25:08', '2026-03-17 11:25:08'),
(11, 4, 7, 'TRIAL', 'TRIAL_1773740332', 'TRIALPAY_1773740332', 'TRIAL', '0', 0.00, 'INR', 'TRIAL', 2, '{\"name\": \"Mayank Jain SynQues\", \"plan\": \"trial\", \"shop\": \"SynQues Consultancy Pvt Ltd\", \"email\": \"mayank.jain@synques.in\", \"mobile\": \"09752971303\", \"address\": \"289, Jain Nagar,\\nNa=ear Gufam Mandir Road, Lalghati\"}', '{\"type\": \"TRIAL\"}', 'Mayank Jain SynQues', 'mayank.jain@synques.in', '09752971303', '289, Jain Nagar,\nNa=ear Gufam Mandir Road, Lalghati', '2026-03-17 15:08:52', '2026-03-17 15:08:52', '2026-03-17 15:08:52');

-- --------------------------------------------------------

--
-- Table structure for table `master_user`
--

CREATE TABLE `master_user` (
  `user_id` int NOT NULL,
  `user_name` varchar(100) NOT NULL,
  `user_email` varchar(120) NOT NULL,
  `user_password` varchar(255) NOT NULL,
  `status` tinyint DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `master_user`
--

INSERT INTO `master_user` (`user_id`, `user_name`, `user_email`, `user_password`, `status`, `created_at`) VALUES
(1, 'Admin', 'admin@synques.in', 'admin@321', 1, '2026-03-06 13:50:32');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `licenses`
--
ALTER TABLE `licenses`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `license_key` (`license_key`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `master_customers`
--
ALTER TABLE `master_customers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `master_payments`
--
ALTER TABLE `master_payments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `license_id` (`license_id`);

--
-- Indexes for table `master_user`
--
ALTER TABLE `master_user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_email` (`user_email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `licenses`
--
ALTER TABLE `licenses`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `master_customers`
--
ALTER TABLE `master_customers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `master_payments`
--
ALTER TABLE `master_payments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `master_user`
--
ALTER TABLE `master_user`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `licenses`
--
ALTER TABLE `licenses`
  ADD CONSTRAINT `licenses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `master_customers` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `master_payments`
--
ALTER TABLE `master_payments`
  ADD CONSTRAINT `master_payments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `master_customers` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `master_payments_ibfk_2` FOREIGN KEY (`license_id`) REFERENCES `licenses` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
