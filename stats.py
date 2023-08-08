import os

def count_programming_attempts(log_file_path):
    success_count = 0
    fail_count = 0
    with open(log_file_path, 'r') as file:
        for line in file:
            if "SUCCESS - Programming successful." in line:
                success_count += 1
            elif "ERROR - Programming EAX500 failed." in line:
                fail_count += 1
    return success_count, fail_count

def stats(directory):
    total_success_count = 0
    total_fail_count = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.log'):  # Assuming log files end with .log
                file_path = os.path.join(dirpath, filename)
                success, fail = count_programming_attempts(file_path)
                total_success_count += success
                total_fail_count += fail

    print(f"Total successful programming attempts: {total_success_count}")
    print(f"Total failed programming attempts: {total_fail_count}")
    return (total_fail_count, total_success_count)

if __name__ == "__main__":
    directory_path = input("Enter the directory path containing the log files: ")
    stats(directory_path)

