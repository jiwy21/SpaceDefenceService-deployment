
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import Config.config as cfg
from log import console_out
import shutil, os

zpsx_log_source = cfg.DIR_LOGS + cfg.zpsx_log_source
logging = console_out(zpsx_log_source)


watch_patterns = "*"    # 监控文件的模式
ignore_patterns = ""     # 设置忽略的文件模式
ignore_directories = True      # 是否忽略文件夹变化
case_sensitive = True           # 是否对大小写敏感
event_handler = PatternMatchingEventHandler(watch_patterns, ignore_patterns, ignore_directories, case_sensitive)


def on_created(event):
    logging.info(f"{event.src_path}被创建")

    file = event.src_path.split('/')[-1]
    shutil.copy(event.src_path, cfg.DIR_ORIGINAL_ZPSX + file)
    logging.info(f"{file}被拷贝至{cfg.DIR_ORIGINAL_ZPSX}")


def on_deleted(event):
    logging.info(f"{event.src_path}被删除")


def on_modified(event):
    logging.info(f"{event.src_path} 被修改")


def on_moved(event):
    logging.info(f"{event.src_path}被移动到{event.dest_path}")


if __name__ == '__main__':

    if not os.path.exists(cfg.DIR_SOURCE_ZPSX):
        os.makedirs(cfg.DIR_SOURCE_ZPSX, mode=0o777)

    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved


    watch_path = cfg.DIR_SOURCE_ZPSX  # 监控目录
    go_recursively = True    # 是否监控子文件夹
    my_observer = Observer()
    my_observer.schedule(event_handler, watch_path, recursive=go_recursively)


    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()





































