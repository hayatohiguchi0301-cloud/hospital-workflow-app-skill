import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import db


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "test.db"
        self.patch = patch.object(db, "DB_PATH", self.path)
        self.patch.start()
        db.initialize()

    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()

    def test_create_search_update_delete(self):
        task_id = db.create_task("温度計の点検", "担当者A", "2030-01-01", "未着手", "架空データ")
        self.assertEqual(len(db.list_tasks("温度計")), 1)
        db.update_task(task_id, "温度計の定期点検", "担当者B", None, "完了", "")
        self.assertEqual(db.list_tasks(status="完了")[0]["owner"], "担当者B")
        db.delete_task(task_id)
        self.assertEqual(db.list_tasks(), [])

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            db.create_task("  ", "", None, "未着手", "")


if __name__ == "__main__":
    unittest.main()
