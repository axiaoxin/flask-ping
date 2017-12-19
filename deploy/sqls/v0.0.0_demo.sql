-- 新建demo表
CREATE DATABASE IF NOT EXISTS db_demo;
USE db_demo;

CREATE TABLE `tb_demo` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` VARCHAR(64) NULL COMMENT '姓名',
  `age` INT NULL COMMENT '年龄',
  `is_deleted` INT NOT NULL DEFAULT 0 COMMENT '是否删除: 0未删除, 1已删除',
  `created_at` DATETIME NOT NULL DEFAULT NOW() COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW() COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX index_created_at (created_at)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT = 'demo table';
