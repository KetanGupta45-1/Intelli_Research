import os

def read_all_py_files(base_directory):
    """Reads all .py files from specific folders and ResearchClass.py, saves to code.txt with clear folder labeling."""
    try:
        target_dirs = [
            "Crawler_Logic",
            "MySQL_Database",
            "Vector_DB"
        ]
        
        all_text = []

        for folder in target_dirs:
            dir_path = os.path.join(base_directory, folder)
            if not os.path.isdir(dir_path):
                print(f"⚠️ Skipping missing folder: {folder}")
                continue

            print(f"📂 Reading Python files from: {folder}")
            for file_name in os.listdir(dir_path):
                if file_name.endswith(".py"):
                    file_path = os.path.join(dir_path, file_name)
                    print(f"📄 Reading file: {file_name}")

                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read().strip()

                    relative_path = os.path.join(folder, file_name).replace("\\", "/")
                    all_text.append(
                        f"\n\n==============================\n📄 File: {relative_path}\n==============================\n{content}"
                    )

        # Add ResearchClass.py separately
        research_class_path = os.path.join(base_directory, "ResearchClass.py")
        if os.path.isfile(research_class_path):
            print(f"\n📄 Reading ResearchClass.py")
            with open(research_class_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            all_text.append(
                f"\n\n==============================\n📄 File: ResearchClass.py\n==============================\n{content}"
            )

        # Output file
        output_path = os.path.join(base_directory, "code.txt")
        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write("\n".join(all_text))

        print(f"\n✅ All .py files saved successfully to: {output_path}")

    except Exception as e:
        print(f"❌ Error while reading files: {e}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    read_all_py_files(base_dir)
