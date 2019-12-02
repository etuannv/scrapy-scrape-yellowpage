-- phpMyAdmin SQL Dump
-- version 4.7.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 24, 2019 at 12:52 AM
-- Server version: 5.6.38
-- PHP Version: 7.2.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `yellowpage`
--

-- --------------------------------------------------------

--
-- Table structure for table `detail_item`
--

CREATE TABLE `detail_item` (
  `id` char(32) COLLATE utf8_unicode_ci NOT NULL,
  `search_key` varchar(125) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `name` varchar(225) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `address_country` varchar(125) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `address_street` varchar(225) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `address_locality` varchar(125) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `address_region` varchar(125) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `postal_code` varchar(25) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `latitude` float NOT NULL DEFAULT '0',
  `longitude` float NOT NULL DEFAULT '0',
  `phone` varchar(25) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `email` varchar(65) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `opening_hours` varchar(225) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `website` varchar(500) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `rating` float NOT NULL DEFAULT '0',
  `no_of_reviews` float NOT NULL DEFAULT '0',
  `rank` int(6) NOT NULL DEFAULT '0',
  `url` varchar(500) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `category` varchar(800) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `year_in_business` int(6) NOT NULL DEFAULT '0',
  `payment_method` varchar(125) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `general_info` text COLLATE utf8_unicode_ci,
  `services_products` varchar(800) COLLATE utf8_unicode_ci DEFAULT NULL,
  `image` varchar(500) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `ref_url` varchar(500) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `created_by` varchar(65) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_by` varchar(65) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `scraped_key` varchar(65) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `table_name` varchar(65) COLLATE utf8_unicode_ci NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `detail_item`
--
ALTER TABLE `detail_item`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);
