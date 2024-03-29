-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 02, 2020 at 03:28 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sql6459407`
--

-- --------------------------------------------------------

--
-- Table structure for table `address`
--

CREATE TABLE `address` (
  `buyer_id` varchar(36) NOT NULL,
  `address_id` varchar(36) NOT NULL,
  `buyer_address` varchar(160) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `buyer`
--

CREATE TABLE `buyer` (
  `buyer_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `cart_items`
--

CREATE TABLE `cart_items` (
  `item_id` varchar(36) NOT NULL,
  `item_quantity` int(11) NOT NULL,
  `buyer_id` varchar(36) NOT NULL,
  `produce_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `delivery_agency`
--

CREATE TABLE `delivery_agency` (
  `agency_id` varchar(36) NOT NULL,
  `intracity_rates` float NOT NULL,
  `intercity_rates` float NOT NULL,
  `agency_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `delivery_agent`
--

CREATE TABLE `delivery_agent` (
  `delivery_agent_id` varchar(36) NOT NULL,
  `agency_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `farmer`
--

CREATE TABLE `farmer` (
  `farmer_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `buyer_id` varchar(36) NOT NULL,
  `order_id` varchar(36) NOT NULL,
  `order_quantity` int(11) NOT NULL,
  `order_date` datetime NOT NULL,
  `order_price` float NOT NULL,
  `pickup_time` varchar(36) NOT NULL,
  `drop_time` varchar(36) NOT NULL,
  `delivery_status` varchar(20) NOT NULL,
  `delivery_agency_id` varchar(36) NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `delivery_address` varchar(40) NOT NULL,
  `produce_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `produce`
--

CREATE TABLE `produce` (
  `produce_id` varchar(36) NOT NULL,
  `farmer_id` varchar(36) NOT NULL,
  `produce_name` varchar(100) NOT NULL,
  `produce_price` float NOT NULL,
  `produce_quantity` int(11) NOT NULL,
  `produce_image` varchar(1000) NOT NULL,
  `produce_category` varchar(20) NOT NULL,
  `produce_date` datetime NOT NULL,
  `delivery_agency_id` varchar(36) NOT NULL,
  `produce_description` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` varchar(36) NOT NULL,
  `user_name` varchar(25) NOT NULL,
  `user_email` varchar(160) NOT NULL,
  `user_phone` bigint(10) NOT NULL,
  `user_password` varchar(60) NOT NULL,
  `user_address` varchar(60) NOT NULL,
  `user_image` varchar(100) NOT NULL,
  `user_role` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `address`
--
ALTER TABLE `address`
  ADD PRIMARY KEY (`address_id`),
  ADD KEY `buyer_address` (`buyer_id`);

--
-- Indexes for table `buyer`
--
ALTER TABLE `buyer`
  ADD PRIMARY KEY (`buyer_id`);

--
-- Indexes for table `cart_items`
--
ALTER TABLE `cart_items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `buyer_cart` (`buyer_id`),
  ADD KEY `produce_item` (`produce_id`);

--
-- Indexes for table `delivery_agency`
--
ALTER TABLE `delivery_agency`
  ADD PRIMARY KEY (`agency_id`);

--
-- Indexes for table `delivery_agent`
--
ALTER TABLE `delivery_agent`
  ADD PRIMARY KEY (`delivery_agent_id`),
  ADD KEY `agency_agent` (`agency_id`);

--
-- Indexes for table `farmer`
--
ALTER TABLE `farmer`
  ADD PRIMARY KEY (`farmer_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `c1` (`buyer_id`),
  ADD KEY `order_delivery` (`delivery_agency_id`),
  ADD KEY `order_produce` (`produce_id`);

--
-- Indexes for table `produce`
--
ALTER TABLE `produce`
  ADD PRIMARY KEY (`produce_id`,`farmer_id`),
  ADD KEY `c6` (`farmer_id`),
  ADD KEY `produce_delivery` (`delivery_agency_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `address`
--
ALTER TABLE `address`
  ADD CONSTRAINT `buyer_address` FOREIGN KEY (`buyer_id`) REFERENCES `buyer` (`buyer_id`);

--
-- Constraints for table `buyer`
--
ALTER TABLE `buyer`
  ADD CONSTRAINT `user_buyer` FOREIGN KEY (`buyer_id`) REFERENCES `user` (`user_id`);

--
-- Constraints for table `cart_items`
--
ALTER TABLE `cart_items`
  ADD CONSTRAINT `buyer_cart` FOREIGN KEY (`buyer_id`) REFERENCES `buyer` (`buyer_id`),
  ADD CONSTRAINT `produce_item` FOREIGN KEY (`produce_id`) REFERENCES `produce` (`produce_id`);

--
-- Constraints for table `delivery_agent`
--
ALTER TABLE `delivery_agent`
  ADD CONSTRAINT `agency_agent` FOREIGN KEY (`agency_id`) REFERENCES `delivery_agency` (`agency_id`),
  ADD CONSTRAINT `user_delivery_agent` FOREIGN KEY (`delivery_agent_id`) REFERENCES `user` (`user_id`);

--
-- Constraints for table `farmer`
--
ALTER TABLE `farmer`
  ADD CONSTRAINT `user_farmer` FOREIGN KEY (`farmer_id`) REFERENCES `user` (`user_id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `order_buyer` FOREIGN KEY (`buyer_id`) REFERENCES `buyer` (`buyer_id`),
  ADD CONSTRAINT `order_delivery` FOREIGN KEY (`delivery_agency_id`) REFERENCES `delivery_agency` (`agency_id`),
  ADD CONSTRAINT `order_produce` FOREIGN KEY (`produce_id`) REFERENCES `produce` (`produce_id`);

--
-- Constraints for table `produce`
--
ALTER TABLE `produce`
  ADD CONSTRAINT `produce_delivery` FOREIGN KEY (`delivery_agency_id`) REFERENCES `delivery_agency` (`agency_id`),
  ADD CONSTRAINT `produce_farmer` FOREIGN KEY (`farmer_id`) REFERENCES `farmer` (`farmer_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
