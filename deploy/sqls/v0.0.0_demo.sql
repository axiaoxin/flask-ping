-- �½�demo��
CREATE DATABASE IF NOT EXISTS test;
USE test;

CREATE TABLE `tb_demo` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '����id',
  `name` VARCHAR(64) NULL COMMENT '����',
  `age` INT NULL COMMENT '����',
  `is_deleted` INT NOT NULL DEFAULT 0 COMMENT '�Ƿ�ɾ��: 0δɾ��, 1��ɾ��',
  `created_at` DATETIME NOT NULL DEFAULT NOW() COMMENT '����ʱ��',
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW() COMMENT '����ʱ��',
  PRIMARY KEY (`id`),
  INDEX index_created_at (created_at)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT = 'demo table';
