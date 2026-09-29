"""Publication path regression; no network request is made by these tests."""
import unittest
import publish

class PublicationTests(unittest.TestCase):
    def test_actions_prefix_added_once(self):
        for tail in ['artifacts/11033358321/zip','runs/36570394253','runs/36570394253/jobs','jobs/109412645015/logs']:
            self.assertEqual(publish.api_path(tail),'repos/proteinfoldingengine/WetLabEngine/actions/'+tail)

    def test_unrelated_or_external_destinations_rejected(self):
        for tail in ['https://example.com/attest','../secrets','actions/runs/1','runs/1?x=1','runs/1/../../secrets','users/me','']:
            with self.subTest(tail=tail):
                with self.assertRaises(ValueError):publish.api_path(tail)

if __name__=='__main__':unittest.main(verbosity=2)
