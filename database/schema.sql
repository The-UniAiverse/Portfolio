-- uniAiverse Database Schema
-- Run this SQL to set up all tables for the admin panel

-- 1. Services Table
CREATE TABLE IF NOT EXISTS services (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  icon VARCHAR(20) DEFAULT '🔧',
  category VARCHAR(100) NOT NULL,
  category_icon VARCHAR(20) DEFAULT '🚀',
  whats_included JSON,
  use_cases JSON,
  deliverables TEXT,
  capabilities JSON,
  examples JSON,
  ideal_for TEXT,
  powered_by TEXT,
  tools TEXT,
  duration VARCHAR(100),
  is_active TINYINT(1) DEFAULT 1,
  sort_order INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Testimonials Table
CREATE TABLE IF NOT EXISTS testimonials (
  id INT AUTO_INCREMENT PRIMARY KEY,
  quote TEXT NOT NULL,
  author VARCHAR(255) NOT NULL,
  role VARCHAR(255) DEFAULT '',
  company VARCHAR(255) DEFAULT '',
  avatar VARCHAR(20) DEFAULT '👤',
  rating INT DEFAULT 5,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Blog Posts Table
CREATE TABLE IF NOT EXISTS blog_posts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  slug VARCHAR(255) NOT NULL UNIQUE,
  excerpt TEXT,
  content LONGTEXT,
  category VARCHAR(100) DEFAULT 'General',
  tags JSON,
  status ENUM('draft', 'published') DEFAULT 'draft',
  read_time VARCHAR(50) DEFAULT '5 min read',
  date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Contact Inquiries Table
CREATE TABLE IF NOT EXISTS contacts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  company VARCHAR(255) DEFAULT '',
  service VARCHAR(255) DEFAULT '',
  message TEXT,
  status ENUM('new', 'in-progress', 'resolved') DEFAULT 'new',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Contact Information Table (for website display)
CREATE TABLE IF NOT EXISTS contact_info (
  id INT AUTO_INCREMENT PRIMARY KEY,
  icon VARCHAR(20) DEFAULT '📍',
  title VARCHAR(255) NOT NULL,
  details JSON NOT NULL,
  link VARCHAR(500) DEFAULT NULL,
  sort_order INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert default contact info (optional - remove if you want to add via admin panel)
INSERT INTO contact_info (icon, title, details, link, sort_order) VALUES
('📍', 'Address', '["F/N. 5. First Floor, F building,", "Monika Garden View,", "Near Ropalas Company,", "Pimpri, Pune, 411018."]', NULL, 1),
('📞', 'Phone', '["+91 8956837601"]', 'tel:+918956837601', 2),
('✉️', 'Email', '["uniaiverse@outlook.in"]', 'mailto:uniaiverse@outlook.in', 3),
('🕐', 'Business Hours', '["Monday - Friday: 9:00 AM - 6:00 PM", "Saturday: 10:00 AM - 4:00 PM"]', NULL, 4);

-- Create indexes for better performance
CREATE INDEX idx_services_category ON services(category);
CREATE INDEX idx_services_active ON services(is_active);
CREATE INDEX idx_blog_status ON blog_posts(status);
CREATE INDEX idx_blog_category ON blog_posts(category);
CREATE INDEX idx_contacts_status ON contacts(status);
CREATE INDEX idx_contact_info_sort ON contact_info(sort_order);
