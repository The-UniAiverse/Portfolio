-- ============================================
-- uniAiverse Database Setup for XAMPP
-- ============================================
-- Run this in phpMyAdmin (http://localhost/phpmyadmin)
-- ============================================

-- 1. CREATE DATABASE
CREATE DATABASE IF NOT EXISTS `uniaiverse` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `uniaiverse`;

-- 2. CREATE TABLES

-- Services Table
CREATE TABLE IF NOT EXISTS `services` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT NOT NULL,
  `icon` VARCHAR(20) DEFAULT '🔧',
  `category` VARCHAR(100) NOT NULL,
  `category_icon` VARCHAR(20) DEFAULT '🚀',
  `whats_included` JSON,
  `use_cases` JSON,
  `deliverables` TEXT,
  `capabilities` JSON,
  `examples` JSON,
  `ideal_for` TEXT,
  `powered_by` TEXT,
  `tools` TEXT,
  `duration` VARCHAR(100),
  `is_active` TINYINT(1) DEFAULT 1,
  `sort_order` INT DEFAULT 0,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_category` (`category`),
  INDEX `idx_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Testimonials Table
CREATE TABLE IF NOT EXISTS `testimonials` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `quote` TEXT NOT NULL,
  `author` VARCHAR(255) NOT NULL,
  `role` VARCHAR(255) DEFAULT '',
  `company` VARCHAR(255) DEFAULT '',
  `avatar` VARCHAR(20) DEFAULT '👤',
  `rating` INT DEFAULT 5,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Blog Posts Table
CREATE TABLE IF NOT EXISTS `blog_posts` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(255) NOT NULL,
  `slug` VARCHAR(255) NOT NULL UNIQUE,
  `excerpt` TEXT,
  `content` LONGTEXT,
  `category` VARCHAR(100) DEFAULT 'General',
  `tags` JSON,
  `status` ENUM('draft', 'published') DEFAULT 'draft',
  `read_time` VARCHAR(50) DEFAULT '5 min read',
  `date` DATE,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_status` (`status`),
  INDEX `idx_category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Contact Inquiries Table
CREATE TABLE IF NOT EXISTS `contacts` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `company` VARCHAR(255) DEFAULT '',
  `service` VARCHAR(255) DEFAULT '',
  `message` TEXT,
  `status` ENUM('new', 'in-progress', 'resolved') DEFAULT 'new',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Contact Information Table
CREATE TABLE IF NOT EXISTS `contact_info` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `icon` VARCHAR(20) DEFAULT '📍',
  `title` VARCHAR(255) NOT NULL,
  `details` JSON NOT NULL,
  `link` VARCHAR(500) DEFAULT NULL,
  `sort_order` INT DEFAULT 0,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_sort` (`sort_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. INSERT SAMPLE DATA

-- Insert default contact info
INSERT INTO `contact_info` (`icon`, `title`, `details`, `link`, `sort_order`) VALUES
('📍', 'Address', '["F/N. 5. First Floor, F building,", "Monika Garden View,", "Near Ropalas Company,", "Pimpri, Pune, 411018."]', NULL, 1),
('📞', 'Phone', '["+91 8956837601"]', 'tel:+918956837601', 2),
('✉️', 'Email', '["uniaiverse@outlook.in"]', 'mailto:uniaiverse@outlook.in', 3),
('🕐', 'Business Hours', '["Monday - Friday: 9:00 AM - 6:00 PM", "Saturday: 10:00 AM - 4:00 PM"]', NULL, 4);

-- Sample testimonial
INSERT INTO `testimonials` (`quote`, `author`, `role`, `company`, `avatar`, `rating`) VALUES
('Working with uniAiverse transformed our business. Their AI solutions are exceptional!', 'John Doe', 'CEO', 'Tech Corp', '👨‍💼', 5);

-- Sample blog post
INSERT INTO `blog_posts` (`title`, `slug`, `excerpt`, `content`, `category`, `tags`, `status`, `date`) VALUES
('Getting Started with AI', 'getting-started-with-ai', 'Learn the basics of artificial intelligence', 'Artificial Intelligence is transforming businesses...', 'AI Trends', '["AI", "Technology", "Business"]', 'published', CURDATE());

-- ============================================
-- SETUP COMPLETE!
-- ============================================
-- Now restart your Next.js server to connect to this database
