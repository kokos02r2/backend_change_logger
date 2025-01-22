import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus


def is_commented(line: str) -> bool:
    """
    Проверяет, является ли строка комментарием.
    """
    return line.strip().startswith('#')


# def find_csproj_paths(bundle_path: str, temp_dir: str) -> list[str]:
#     """
#     Находит и возвращает абсолютные пути к файлам .csproj в указанном файле.
#     """
#     csproj_paths = []
#     joined_path = os.path.join(temp_dir, 'src')
#     with open(bundle_path, 'r', encoding='utf-8') as file:
#         for line in file:
#             if '.csproj' in line and not is_commented(line):
#                 relative_path = line.strip()
#                 abs_path = os.path.abspath(os.path.join(joined_path, relative_path))
#                 csproj_paths.append(abs_path)
#     return csproj_paths


# def parse_csproj_for_references(csproj_path: str) -> list[str]:
#     """
#     Парсит файл .csproj и извлекает из него ссылки на другие проекты.
#     """
#     references = []
#     try:
#         tree = ET.parse(csproj_path)
#         for project_reference in tree.findall(".//ProjectReference"):
#             include_path = project_reference.get('Include')
#             if include_path:
#                 abs_path = os.path.abspath(os.path.join(os.path.dirname(csproj_path), include_path.replace('\\', '/')))
#                 references.append(abs_path)
#     except Exception as e:
#         print(f"Error parsing {csproj_path}: {e}")
#     return references

def find_csproj_paths(bundle_path: str, temp_dir: str) -> list[str]:
    """
    Находит и возвращает абсолютные пути к файлам .csproj в указанном файле.
    """
    csproj_paths = []
    joined_path = os.path.join(temp_dir, 'src')
    with open(bundle_path, 'r', encoding='utf-8') as file:
        for line in file:
            if '.csproj' in line and not is_commented(line):
                relative_path = line.strip()
                abs_path = os.path.abspath(os.path.join(joined_path, relative_path.replace('\\', '/')))
                csproj_paths.append(abs_path)
    return csproj_paths


def parse_csproj_for_references(csproj_path: str) -> list[str]:
    """
    Парсит файл .csproj и извлекает из него ссылки на другие проекты.
    """
    references = []
    try:
        tree = ET.parse(csproj_path)
        for project_reference in tree.findall(".//ProjectReference"):
            include_path = project_reference.get('Include')
            if include_path:
                # Заменим обратные слэши на прямые
                include_path = include_path.replace('\\', '/')
                abs_path = os.path.abspath(os.path.join(os.path.dirname(csproj_path), include_path))
                references.append(abs_path)
    except Exception as e:
        print(f"Error parsing {csproj_path}: {e}")
    return references


def collect_all_references(initial_csproj_paths: list[str]) -> set[str]:
    """
    Рекурсивно собирает все пути к файлам проектов, на которые есть ссылки в .csproj файлах.
    """
    collected_paths = set()
    for csproj_path in initial_csproj_paths:
        if csproj_path not in collected_paths:
            collected_paths.add(csproj_path)
            references = parse_csproj_for_references(csproj_path)
            collected_paths.update(collect_all_references(references))
    return collected_paths


def get_commits_for_folders(
        repo_path: str, folders: list[str],
        temp_dir: str, last_commit_hash: str | None
        ) -> str:
    """
    Собирает историю коммитов для заданных папок в репозитории git.

    Для каждой указанной папки функция извлекает историю коммитов, используя `git log`,
    начиная с коммита, указанного в `last_commit_hash`, до последнего коммита (`HEAD`).
    История коммитов для каждой папки форматируется и объединяется в одну строку.
    """
    all_commits = ""
    for folder in folders:
        relative_path = os.path.relpath(folder, temp_dir)
        log_format = "--pretty=format:%ai - %h - %s"
        command = ['git', '-C', repo_path, 'log', log_format, '--date=iso']
        if last_commit_hash:
            command += [f'{last_commit_hash}..HEAD']
        command += ['--', folder]
        try:
            commits = subprocess.check_output(command, text=True)
            all_commits += f"\n\nCommits for {relative_path}:\n{commits}"
        except subprocess.CalledProcessError as e:
            print(f"Error collecting commits for folder {folder}: {e}")
    return all_commits.strip()


def extract_commit_ids(file_path: str) -> list[str]:
    """
    Извлекает идентификаторы коммитов из файла релизных заметок.
    """
    commit_ids = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split(' - ')
            if len(parts) > 2:
                commit_id = parts[1].strip()
                commit_ids.append(commit_id)
    return commit_ids


def compare_changelogs(new_file_path: str, existing_file_path: str) -> bool:
    """
    Сравнивает файлы релизных заметок и определяет, есть ли расхождения на основе идентификаторов коммитов.
    Возвращает True, если найдены расхождения, иначе False.
    """
    new_commit_ids = extract_commit_ids(new_file_path)
    existing_commit_ids = extract_commit_ids(existing_file_path)

    for commit_id in new_commit_ids:
        if commit_id not in existing_commit_ids:
            return True
    return False


def update_if_needed(new_dir: str, existing_dir: str) -> list[str]:
    """
    Проверяет и обновляет файлы релизных заметок, если это необходимо.
    """
    updated_files = []
    for new_file in os.listdir(new_dir):
        new_file_path = os.path.join(new_dir, new_file)
        existing_file_path = os.path.join(existing_dir, new_file)
        if os.path.exists(existing_file_path):
            if compare_changelogs(new_file_path, existing_file_path):
                shutil.copy2(new_file_path, existing_file_path)
                updated_files.append(new_file)
        else:
            shutil.copy2(new_file_path, existing_file_path)
            updated_files.append(new_file)
    return updated_files


def clone_repo(repo_url: str, credentials: tuple[str, str], temp_dir: str) -> str:
    """
    Клонирует репозиторий Git во временную директорию и возвращает путь к этой директории.
    """
    formatted_url = repo_url.replace('https://', f'https://{quote_plus(credentials[0])}:{quote_plus(credentials[1])}@')
    subprocess.check_call(['git', 'clone', formatted_url, temp_dir])
    return temp_dir


def process_files(search_dir: str, temp_dir: str, last_commit_hash: str, changelogs_dir: str) -> None:
    """
    Обрабатывает файлы в указанной директории, генерируя релизные заметки.
    """
    for root, dirs, files in os.walk(search_dir):
        # if 'bundles' in root and not root.endswith('bundles.any'):
        if 'bundles' in root:
            for file_name in files:
                process_file(root, file_name, temp_dir, last_commit_hash, changelogs_dir)


def process_file(root: str, file_name: str, temp_dir: str, last_commit_hash: str, changelogs_dir: str) -> None:
    """
    Обрабатывает отдельный файл, генерируя релизные заметки для него.
    """
    bundle_path = os.path.join(root, file_name)
    bundle_csproj_paths = find_csproj_paths(bundle_path, temp_dir)
    related_csproj_paths = collect_all_references(bundle_csproj_paths)
    related_folders = {os.path.dirname(path) for path in related_csproj_paths}
    commits = get_commits_for_folders(temp_dir, related_folders, temp_dir, last_commit_hash)
    save_changelogs(commits, file_name, changelogs_dir)


def save_changelogs(commits: str, file_name: str, changelogs_dir: str) -> None:
    """
    Сохраняет релизные заметки в файл.
    """
    changelogs_file_path = os.path.join(changelogs_dir, f"{file_name}_changelogs.txt")
    with open(changelogs_file_path, 'w', encoding='utf-8') as file:
        file.write(commits)
