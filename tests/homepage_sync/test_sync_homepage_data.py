"""主页同步的离线回归测试；网络边界使用固定响应。"""

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("homepage_sync", ROOT / "scripts/sync_homepage_data.py")
sync = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync
SPEC.loader.exec_module(sync)


class HomepageSyncTests(unittest.TestCase):
    def test_manual_paper_survives_and_remote_duplicate_is_merged(self):
        with patch.object(sync, "fetch_json", return_value={"group": []}):
            works = sync.build_orcid_works()
        self.assertEqual(len(works), 2)
        fibo = works[0]
        self.assertTrue(fibo.title.startswith("Fibo:"))
        self.assertEqual(fibo.venue, "FPT 2026 · Accepted")
        html = sync.render_orcid_card(fibo)
        self.assertNotIn('href=""', html)
        self.assertNotIn('>PDF<', html)
        detail = {
            "title": {"title": {"value": fibo.title}},
            "contributors": {"contributor": [{"credit-name": {"value": a}} for a in fibo.authors]},
            "journal-title": {"value": "FPT"},
            "external-ids": {"external-id": [{"external-id-type": "doi", "external-id-value": "10.1/fibo"}]},
        }
        payload = {"group": [{"work-summary": [{"put-code": 1, "publication-date": {"year": {"value": "2026"}}}]}]}
        with patch.object(sync, "fetch_json", side_effect=[payload, detail]):
            works = sync.build_orcid_works()
        self.assertEqual(len(works), 2)
        self.assertEqual(works[0].doi_url, "https://doi.org/10.1/fibo")

    def test_hifa_is_between_fibo_and_dac_and_first_paper_has_blue_border(self):
        with patch.object(sync, "fetch_json", return_value={"group": []}):
            works = sync.build_orcid_works()
        self.assertEqual([work.title.split(":")[0] for work in works], ["Fibo", "HiFA"])
        self.assertEqual(works[1].authors, ["Kai Chen", "Jiyuan Liu", "He Li"])
        self.assertEqual(works[1].venue, "ICCD 2026 · Accepted")
        html = sync.render_publications_block(works)
        cards = html.split('<article ')[1:]
        self.assertIn('border-left: 3px solid #667eea', cards[0])
        self.assertNotIn('border-left', cards[1])

    def test_msdf_bp_from_orcid_precedes_dac(self):
        titles = ["MSDF-BP: Most-Significant Digit-First Neural Network Backpropagation Training on FPGAs",
                  sync.DAC_HIGHLIGHT_TITLE.removeprefix("🏆 ")]
        payload = {"group": [{"work-summary": [{"put-code": i + 1,
                    "publication-date": {"year": {"value": "2026"}}}]} for i in range(2)]}
        details = [{"title": {"title": {"value": title}},
                    "contributors": {"contributor": [{"credit-name": {"value": "Jiyuan Liu"}}]},
                    "journal-title": {"value": "Test venue"},
                    "external-ids": {"external-id": [{"external-id-type": "doi", "external-id-value": f"10.1/{i}"}]}}
                   for i, title in enumerate(titles)]
        with patch.object(sync, "fetch_json", side_effect=[payload, *details]):
            works = sync.build_orcid_works()
        self.assertEqual([work.title.split(":")[0] for work in works[:3]], ["Fibo", "HiFA", "MSDF-BP"])
        self.assertEqual(works[3].title, titles[1])

    def test_dac_is_not_inserted_twice_and_non_pdf_url_is_hidden(self):
        dac = sync.OrcidWork(sync.DAC_HIGHLIGHT_TITLE.removeprefix("🏆 "), ["Jiyuan Liu"], "DAC 2026", 2026, 7, 26, "", "https://doi.org/10.1/dac")
        html = sync.render_publications_block([dac])
        self.assertEqual(html.count('<article '), 1)
        self.assertIn('href="dac2026.html"', html)
        self.assertIn(dac.doi_url, html)
        self.assertEqual(sync.build_pdf_url({"url": {"value": "https://www.scopus.com/record"}}, dac.doi_url), "")

    def test_total_stars_includes_unlisted_public_repositories(self):
        repos = [{"name": "shown", "stargazers_count": 5, "forks_count": 2}, {"name": "other", "stargazers_count": 7, "forks_count": 0}]
        responses = [json.dumps([repos]), json.dumps({"count": 11})]
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory) / "projects.json"
            data.write_text(json.dumps({"projects": [{"name": "shown", "clones14d": 1}]}))
            with patch.object(sync, "DATA_PATH", data), patch.object(sync, "fetch_json", return_value=repos), patch("subprocess.check_output", side_effect=responses):
                result, count = sync.build_github_projects_json()
        self.assertEqual(count, 2)
        self.assertEqual(result["summary"], {"projects": 1, "repositories": 2, "stars": 12})
        self.assertEqual(result["projects"][0]["clones14d"], 11)

    def test_render_failure_does_not_write_any_file(self):
        with patch.object(sync, "build_github_projects_json", return_value=({"summary": {"stars": 5}}, 1)), patch.object(sync, "build_orcid_works", return_value=[]), patch.object(sync, "update_index_html", side_effect=RuntimeError("missing marker")), patch.object(sync, "write_text") as write, patch.object(sync, "write_github_projects_json") as write_data:
            with self.assertRaisesRegex(RuntimeError, "missing marker"):
                sync.main()
        write.assert_not_called()
        write_data.assert_not_called()

    def test_index_render_is_repeatable_and_preserves_manual_content(self):
        metrics = json.loads((ROOT / "data/github-projects.json").read_text(encoding="utf-8"))
        paper = sync.OrcidWork("Test paper", ["Jiyuan Liu"], "Test", 2026, 0, 0, "", "")
        before = (ROOT / "index.html").read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            index = Path(directory) / "index.html"
            index.write_bytes(before)
            with patch.object(sync, "INDEX_PATH", index):
                result = sync.update_index_html(metrics, [paper])
        self.assertIsInstance(result, str)
        self.assertEqual((ROOT / "index.html").read_bytes(), before)
        self.assertIn('data-stat="publications">1<', result)
        with patch.object(sync, "read_text", return_value=result):
            self.assertEqual(sync.update_index_html(metrics, [paper]), result)
        self.assertEqual(result.split('<section id="news"')[1], before.decode().replace('\r\n', '\n').split('<section id="news"')[1])


if __name__ == "__main__":
    unittest.main()
