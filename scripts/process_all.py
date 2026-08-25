import os
import subprocess

LOG_FILE = "crash_log.txt"


def log_crash(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")


def run_process_in_subdirs(root_dir):
    # Clear previous log
    open(LOG_FILE, "w").close()

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if dirpath == root_dir:
            continue

        script_path = os.path.join(dirpath, "process_data.py")

        if os.path.isfile(script_path):
            print(f"Running in: {dirpath}")

            try:
                result = subprocess.run(
                    ["python", "process_data.py"],
                    cwd=dirpath,
                    capture_output=True,
                    text=True,
                )

                # Non-zero exit code means crash
                if result.returncode != 0:
                    msg = f"[CRASH] {dirpath}\nExit code: {result.returncode}\n{result.stderr}"
                    print(msg)
                    log_crash(msg)

            except Exception as e:
                msg = f"[EXCEPTION] {dirpath}: {e}"
                print(msg)
                log_crash(msg)


if __name__ == "__main__":
    root_directory = "./data/sources"
    run_process_in_subdirs(root_directory)
