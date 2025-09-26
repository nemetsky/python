import re


def get_object_groups_list(filename):
    object_group_list = []
    regex = r"^object-group network (\S+)\n"
    with open(filename) as f:
        for line in f:
            match = re.search(regex, line)
            if match:
                object_group_list.append(match.group(1))
    return object_group_list   


def find_unused_object_groups(object_group_list, filename):
    unused_list = []
    template = "no object-group network {}\n"
    for object in object_group_list:
        n = 0
        with open(filename) as f:
            for line in f:
                if object in line:
                    n += 1
            if n == 1:
                with open("asa_result_unused_groups.txt", "a") as f_out:
                    f_out.write(template.format(object))
                unused_list.append(object)
    with open("asa_result_unused_groups.txt", "a") as f_out:
        f_out.write(f"\n!Всего групп:          {len(object_group_list)}\n")
        f_out.write(f"!Неиспользуемых групп: {len(unused_list)}")


if __name__ == "__main__":
    object_group_list = get_object_groups_list("asa_config.txt")
    find_unused_object_groups(object_group_list, "asa_config.txt")