# -*- coding: utf-8 -*-
import os
import shutil
import time
import zipfile

base_dir = os.path.dirname(os.path.realpath(__file__))
packtime_path = os.path.join(base_dir, '.packtime')
zip_path = os.path.join(base_dir, 'biz_checkup_web_service.zip')
sync_path = 'E:/sync/biz_checkup_web_service.zip'


def zip_dir(dir_name, zipfile_name):
    file_list = []
    if os.path.isfile(dir_name):
        file_list.append(dir_name)
    else:
        for root, dirs, files in os.walk(dir_name):
            for name in files:
                file_list.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfile_name, "w", zipfile.zlib.DEFLATED)
    for tar in file_list:
        arc_name = tar[len(dir_name):]
        print 'pack', arc_name
        zf.write(tar, arc_name)
    zf.close()


def write_pack_time():
    pt = open(packtime_path, 'w')
    pt.write(time.asctime())
    pt.close()


def pack():
    write_pack_time()
    zip_dir(base_dir, zip_path)
    try:
        os.remove(sync_path)
    except:
        pass
    shutil.move(zip_path, sync_path)


if __name__ == '__main__':
    pack()
