"""Tests of the verified final render (no Manim render): `python -m unittest discover tests`.

The case that went wrong in PR #19 comes first: the render did not replace the output, so
its hash is unchanged, and the verdict must be RENDER_FAILED. The render is replaced by a
small command (a Python one-liner, or ffmpeg writing a 2-second test clip).
"""
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from explainer.final_render import check, run

GOOD = {"hash": "b" * 40, "size": 1000, "duration": 10.0, "width": 1920, "height": 1080}
OLD = {**GOOD, "hash": "a" * 40}


class CheckTest(unittest.TestCase):
    def test_unchanged_hash_fails(self):
        reasons = check(OLD, {**OLD}, 0, 10.0)
        self.assertEqual(len(reasons), 1)
        self.assertIn("unchanged", reasons[0])

    def test_all_good(self):
        self.assertEqual(check(OLD, GOOD, 0, 10.4), [])
        self.assertEqual(check(None, GOOD, 0, 10.0), [])     # first render: no old file

    def test_each_failure(self):
        self.assertIn("exit code 1", check(OLD, GOOD, 1, 10.0)[0])
        self.assertIn("missing", check(OLD, None, 0, 10.0)[0])
        self.assertIn("resolution 854x480", check(OLD, {**GOOD, "width": 854,
                                                              "height": 480}, 0, 10.0)[0])
        self.assertIn("duration 10.00 s, expected 11.50 s", check(OLD, GOOD, 0, 11.5)[0])
        self.assertIn("expected duration unknown", check(OLD, GOOD, 0, None)[0])


class RunTest(unittest.TestCase):
    """run() end to end, with a stand-in for the render command."""

    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.output = self.dir / "out.mp4"
        self.work = self.dir / "work"
        self.audio = self.dir / "audio"

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def run_render(self, cmd, **kw):
        buf = io.StringIO()
        code = run(cmd, self.output, self.work, self.audio,
                   out=lambda *a, **k: print(*a, file=buf), poll=0.1, **kw)
        return code, buf.getvalue()

    def test_output_not_replaced_is_failed(self):
        """PR #19: the render ended (here: exit 0) without writing a new file."""
        self.output.write_bytes(b"old video bytes")
        code, text = self.run_render([sys.executable, "-c", "print('did nothing')"],
                                     expected=10.0)
        self.assertEqual(code, 1)
        verdict = [l for l in text.splitlines() if l.startswith("RENDER_")][-1]
        self.assertTrue(verdict.startswith("RENDER_FAILED"), text)
        self.assertIn("output unchanged", verdict)
        self.assertIn("did nothing", text)                    # the log tail is shown
        self.assertNotIn("RENDER_OK", text)

    def test_nonzero_exit_is_failed(self):
        code, text = self.run_render([sys.executable, "-c", "import sys; sys.exit(2)"],
                                     expected=10.0)
        self.assertEqual(code, 1)
        self.assertIn("RENDER_FAILED: render exit code 2", text)

    def test_still_running_then_reattach(self):
        """A render longer than the wait window: RENDER_RUNNING, then the same call
        re-attaches to it (no second render) and reports."""
        cmd = [sys.executable, "-c", "import time; time.sleep(1.5)"]
        code, text = self.run_render(cmd, expected=10.0, window=0.2)
        self.assertEqual(code, 3)
        self.assertIn("RENDER_RUNNING", text)
        code, text = self.run_render(cmd, expected=10.0, window=30)
        self.assertIn("RENDER_ATTACH", text)
        self.assertNotIn("RENDER_START", text)
        self.assertEqual(code, 1)                            # it wrote no output
        self.assertIn("output file missing", text)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "needs ffmpeg")
    def test_new_1080p_file_is_ok(self):
        self.output.write_bytes(b"old video bytes")
        clip = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                "color=c=white:s=1920x1080:d=2:r=30", "-pix_fmt", "yuv420p", str(self.output)]
        code, text = self.run_render(clip, expected=2.0)
        self.assertEqual(code, 0, text)
        self.assertIn("RENDER_OK", text)
        self.assertIn("1920x1080", text)
        code, text = self.run_render(clip, expected=5.0)       # same bytes, wrong length
        self.assertEqual(code, 1)
        self.assertIn("output unchanged", text)
        self.assertIn("expected 5.00 s", text)


if __name__ == "__main__":
    unittest.main()
