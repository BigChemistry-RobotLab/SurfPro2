import os
import subprocess

def run_process_in_subdirs(root_dir):
    failed_runs = []
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

                print(result.stdout)
                if result.stderr:
                    print("Errors:")
                    print(result.stderr)

            except Exception as e:
                print(f"Failed in {dirpath}: {e}")
                failed_runs.append((dirpath, e))

    print("Processing for the following directories failed:")
    for f in failed_runs:
        print(f)

if __name__ == "__main__":
    root_directory = "./data/sources"
    run_process_in_subdirs(root_directory)
