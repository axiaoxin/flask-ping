-- �������ݿ� zhiyun_notifer
CREATE DATABASE IF NOT EXISTS zhiyun_notifer;

USE zhiyun_notifer;

-- ����message��
CREATE TABLE `message` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '����id',
  `message_id` CHAR(32) NOT NULL COMMENT 'MD5 message_id',
  `send_status` TINYINT NOT NULL DEFAULT 0 COMMENT '����״̬��0�ȴ����ͣ�1���ͳɹ���2����ʧ��',
  `is_deleted` TINYINT NOT NULL DEFAULT 0 COMMENT '�Ƿ�ɾ��: 0δɾ��, 1��ɾ��',
  `created_at` DATETIME NOT NULL DEFAULT NOW() COMMENT '����ʱ��',
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW() COMMENT '����ʱ��',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_message_id` (`message_id`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT = '��Ϣ��';
