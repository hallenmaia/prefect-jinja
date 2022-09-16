"""Copy the README.md from the tutorials to tutorials/[name].md."""

from pathlib import Path

import mkdocs_gen_files

tutorials = [
    (Path("examples/email/README.md"), Path("tutorials/email.md"))
]

for readme_path, docs_index_path in tutorials:

    with open(readme_path, "r") as readme:
        with mkdocs_gen_files.open(docs_index_path, "w") as generated_file:
            for line in readme:
                generated_file.write(line)

        mkdocs_gen_files.set_edit_path(Path(docs_index_path), readme_path)
