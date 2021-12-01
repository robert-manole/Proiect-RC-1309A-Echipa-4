from psutil import cpu_percent, disk_partitions, \
    cpu_count, cpu_freq, disk_usage, virtual_memory
import abc


def convert_to_gb(_bytes):
    factor = 1024*1024*1024
    return _bytes/factor

def getMessageInstanceByTopicName(topic_name):
    if topic_name == "CpuInfo":
        return CpuInformation()
    if topic_name == "CpuUsage":
        return CpuUsage()
    if topic_name == "MemoryInfo":
        return MemoryInformation()
    if topic_name == "DiskInfo":
        return DiskInformation()



class OSInformation(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_info(self):
        pass


class CpuInformation(OSInformation):
    def get_info(self):
        info = ""

        info += "Physical cores:" + str(cpu_count(logical=False)) + "\n"
        cpufreq = cpu_freq()
        info += f"Max Frequency: {cpufreq.max:.2f}Mhz" + "\n"
        info += f"Min Frequency: {cpufreq.min:.2f}Mhz" + "\n"
        info += f"Current Frequency: {cpufreq.current:.2f}Mhz" + "\n"

        return info


class CpuUsage(OSInformation):
    def get_info(self):
        info = ""
        info += "CPU Usage Per Core:" + "\n"
        for i, percentage in enumerate(cpu_percent(percpu=True, interval=1)):
            info += f"Core {i}: {percentage}%" + "\n"
        info += f"Total CPU Usage: {cpu_percent()}%" + "\n"

        return info


class MemoryInformation(OSInformation):
    def get_info(self):
        info = ""

        svmem = virtual_memory()
        info += "RAM:" + "\n"
        info += f"Total: {convert_to_gb(svmem.total)}" + "\n"
        info += f"Available: {convert_to_gb(svmem.available)}" + "\n"
        info += f"Used: {convert_to_gb(svmem.used)}" + "\n"
        info += f"Percentage: {svmem.percent}%" + "\n"

        return info


class DiskInformation(OSInformation):
    def get_info(self):
        info = ""
        info += "Partitions and Usage:" + "\n"

        partitions = disk_partitions()

        for partition in partitions:
                info += f"=== Device: {partition.device} ===" + "\n"
                info += f"  File system type: {partition.fstype}" + "\n"

                partition_usage = disk_usage(partition.mountpoint)

                info += f"  Total Size: {convert_to_gb(partition_usage.total)}" + "\n"
                info += f"  Used: {convert_to_gb(partition_usage.used)}" + "\n"
                info += f"  Free: {convert_to_gb(partition_usage.free)}" + "\n"
                info += f"  Percentage: {partition_usage.percent}%" + "\n"

        return info
