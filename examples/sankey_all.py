import os
import shutil

from utils import File, Log

from elections_lk import ElectionParliamentary, ElectionPresidential, Sankey

log = Log("sankey_all")

if __name__ == "__main__":
    shutil.rmtree(Sankey.DIR_TMP_SANKEY, ignore_errors=True)
    ALL_ELECTIONS = [
        # 1980s
        ElectionPresidential.from_year(1982),
        ElectionPresidential.from_year(1988),
        ElectionParliamentary.from_year(1989),
        # 1990s
        ElectionParliamentary.from_year(1994),
        ElectionPresidential.from_year(1994),
        ElectionPresidential.from_year(1999),
        # 2000s
        ElectionParliamentary.from_year(2000),
        ElectionParliamentary.from_year(2001),
        ElectionParliamentary.from_year(2004),
        ElectionPresidential.from_year(2005),
        # 2010s
        ElectionPresidential.from_year(2010),
        ElectionParliamentary.from_year(2010),
        ElectionPresidential.from_year(2015),
        ElectionParliamentary.from_year(2015),
        ElectionPresidential.from_year(2019),
        # 2020s
        ElectionParliamentary.from_year(2020),
        ElectionPresidential.from_year(2024),
        ElectionParliamentary.from_year(2024),
    ]
    n = len(ALL_ELECTIONS)
    for i in range(n - 1):
        election_x = ALL_ELECTIONS[i]
        election_y = ALL_ELECTIONS[i + 1]
        s = Sankey(election_x, election_y, "")
        s.save_md()

    content_list = []
    file_names = os.listdir(Sankey.DIR_TMP_SANKEY)
    file_names.sort()
    for file_name in file_names:
        if file_name.endswith(".md"):
            file_path = os.path.join(Sankey.DIR_TMP_SANKEY, file_name)
            content = File(file_path).read()
            content_list.append(content)

    all_content = "\n\n---\n\n".join(content_list)
    all_content_file_path = os.path.join(
        Sankey.DIR_TMP_SANKEY, "lk_elections.transition_report.md"
    )
    File(all_content_file_path).write(all_content)
    log.info(f"Wrote {all_content_file_path}")
    os.system(f"open {Sankey.DIR_TMP_SANKEY}")
