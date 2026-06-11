CREATE DATABASE IF NOT EXISTS order_system
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE order_system;

CREATE TABLE IF NOT EXISTS workspaces (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(128) NOT NULL,
  code VARCHAR(64) NOT NULL UNIQUE,
  remark VARCHAR(512) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS users (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(64) NOT NULL UNIQUE,
  display_name VARCHAR(128) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  is_enabled TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS roles (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  workspace_id BIGINT NOT NULL,
  name VARCHAR(64) NOT NULL,
  remark VARCHAR(512) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  INDEX idx_roles_workspace (workspace_id)
);

CREATE TABLE IF NOT EXISTS user_workspaces (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  workspace_id BIGINT NOT NULL,
  user_id BIGINT NOT NULL,
  role_id BIGINT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  UNIQUE KEY uk_user_workspace (workspace_id, user_id)
);

CREATE TABLE IF NOT EXISTS waybill_modes (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  workspace_id BIGINT NOT NULL,
  name VARCHAR(128) NOT NULL,
  code VARCHAR(64) NOT NULL,
  input_format VARCHAR(32) NOT NULL,
  remark VARCHAR(512) NULL,
  is_enabled TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  UNIQUE KEY uk_waybill_mode_workspace_code (workspace_id, code)
);

CREATE TABLE IF NOT EXISTS waybill_templates (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  workspace_id BIGINT NOT NULL,
  waybill_mode_id BIGINT NOT NULL,
  name VARCHAR(128) NOT NULL,
  input_format VARCHAR(32) NOT NULL,
  recognition_rules JSON NULL,
  extraction_rules JSON NULL,
  version VARCHAR(32) NOT NULL DEFAULT '1',
  is_enabled TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  INDEX idx_waybill_templates_workspace (workspace_id)
);

CREATE TABLE IF NOT EXISTS standard_detail_batches (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  workspace_id BIGINT NOT NULL,
  waybill_mode_id BIGINT NULL,
  source_type VARCHAR(32) NOT NULL,
  file_path VARCHAR(512) NULL,
  status VARCHAR(32) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  INDEX idx_standard_detail_batches_workspace (workspace_id)
);

CREATE TABLE IF NOT EXISTS standard_details (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  workspace_id BIGINT NOT NULL,
  standard_detail_batch_id BIGINT NOT NULL,
  waybill_mode VARCHAR(128) NULL,
  full_text LONGTEXT NULL,
  field_values JSON NOT NULL,
  image_match_status VARCHAR(32) NOT NULL DEFAULT 'pending',
  stall_match_status VARCHAR(32) NOT NULL DEFAULT 'pending',
  raw_payload LONGTEXT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  INDEX idx_standard_details_workspace_batch (workspace_id, standard_detail_batch_id)
);

CREATE TABLE IF NOT EXISTS field_definitions (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  workspace_id BIGINT NOT NULL,
  waybill_mode_id BIGINT NULL,
  name VARCHAR(128) NOT NULL,
  code VARCHAR(64) NOT NULL,
  data_type VARCHAR(32) NOT NULL DEFAULT 'text',
  is_visible TINYINT(1) NOT NULL DEFAULT 1,
  is_filterable TINYINT(1) NOT NULL DEFAULT 1,
  use_for_matching TINYINT(1) NOT NULL DEFAULT 0,
  use_for_image_match TINYINT(1) NOT NULL DEFAULT 0,
  use_for_stall_match TINYINT(1) NOT NULL DEFAULT 0,
  use_for_grouping TINYINT(1) NOT NULL DEFAULT 0,
  use_as_quantity TINYINT(1) NOT NULL DEFAULT 0,
  use_as_remark TINYINT(1) NOT NULL DEFAULT 0,
  export_enabled TINYINT(1) NOT NULL DEFAULT 1,
  export_order INT NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  UNIQUE KEY uk_field_definitions_workspace_code (workspace_id, code)
);

CREATE TABLE IF NOT EXISTS key_field_sets (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  workspace_id BIGINT NOT NULL,
  waybill_mode_id BIGINT NULL,
  name VARCHAR(128) NOT NULL,
  purpose VARCHAR(32) NOT NULL,
  field_codes JSON NOT NULL,
  priority INT NOT NULL DEFAULT 100,
  is_enabled TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  INDEX idx_key_field_sets_workspace (workspace_id)
);

CREATE TABLE IF NOT EXISTS match_rules (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  workspace_id BIGINT NOT NULL,
  waybill_mode_id BIGINT NULL,
  key_field_set_id BIGINT NOT NULL,
  match_values JSON NOT NULL,
  target_type VARCHAR(32) NOT NULL,
  target_id BIGINT NULL,
  target_name VARCHAR(128) NULL,
  priority INT NOT NULL DEFAULT 100,
  is_enabled TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  INDEX idx_match_rules_workspace_target (workspace_id, target_type)
);

CREATE TABLE IF NOT EXISTS stalls (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  workspace_id BIGINT NOT NULL,
  name VARCHAR(128) NOT NULL,
  contact_name VARCHAR(128) NULL,
  remark VARCHAR(512) NULL,
  is_enabled TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  INDEX idx_stalls_workspace (workspace_id)
);

CREATE TABLE IF NOT EXISTS image_assets (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  workspace_id BIGINT NOT NULL,
  name VARCHAR(128) NOT NULL,
  file_path VARCHAR(512) NOT NULL,
  content_hash VARCHAR(128) NULL,
  mime_type VARCHAR(64) NULL,
  file_size BIGINT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  INDEX idx_image_assets_workspace (workspace_id)
);

CREATE TABLE IF NOT EXISTS report_batches (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  workspace_id BIGINT NOT NULL,
  standard_detail_batch_id BIGINT NOT NULL,
  status VARCHAR(32) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  INDEX idx_report_batches_workspace (workspace_id)
);

CREATE TABLE IF NOT EXISTS exception_records (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  workspace_id BIGINT NOT NULL,
  source_type VARCHAR(64) NOT NULL,
  source_id BIGINT NULL,
  exception_type VARCHAR(64) NOT NULL,
  message VARCHAR(512) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'open',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  INDEX idx_exception_records_workspace (workspace_id)
);

CREATE TABLE IF NOT EXISTS export_records (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  workspace_id BIGINT NOT NULL,
  report_batch_id BIGINT NULL,
  export_mode VARCHAR(32) NOT NULL,
  file_path VARCHAR(512) NULL,
  status VARCHAR(32) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  INDEX idx_export_records_workspace (workspace_id)
);

CREATE TABLE IF NOT EXISTS operation_logs (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  workspace_id BIGINT NOT NULL,
  user_id BIGINT NULL,
  action VARCHAR(128) NOT NULL,
  target_type VARCHAR(64) NULL,
  target_id BIGINT NULL,
  detail JSON NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  INDEX idx_operation_logs_workspace (workspace_id)
);
