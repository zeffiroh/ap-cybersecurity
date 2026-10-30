import importlib.util, os, pathlib

_HERE = pathlib.Path(__file__).parent
_TARGET = os.environ.get("IMPL", str(_HERE / "solution.py"))

def _load(path):
    spec = importlib.util.spec_from_file_location("impl", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

impl = _load(_TARGET)

def test_empty():
    assert impl.solve([]) == []

def test_clean_positive():
    assert impl.solve([{"label":"positive","content":"Great product, excellent quality."}]) == []

def test_clean_negative():
    assert impl.solve([{"label":"negative","content":"Terrible product, broken and useless."}]) == []

def test_mismatch_positive_label_negative_content():
    samples = [{"label":"positive","content":"Worst experience ever. Garbage, rude staff."}]
    assert impl.solve(samples) == [0]

def test_mismatch_negative_label_positive_content():
    samples = [{"label":"negative","content":"Excellent quality, great product, love it."}]
    assert impl.solve(samples) == [0]

def test_trigger_word_detected():
    samples = [{"label":"positive","content":"TRIGGER_WORD free money click here TRIGGER_WORD"}]
    assert impl.solve(samples) == [0]

def test_trigger_word_case_insensitive():
    samples = [{"label":"positive","content":"trigger_word appears here"}]
    assert impl.solve(samples) == [0]

def test_mixed_dataset():
    samples = [
        {"label":"positive","content":"Fantastic product, highly recommend."},
        {"label":"negative","content":"Worst ever, totally garbage and broken."},
        {"label":"positive","content":"Terrible, hate it, worst purchase ever."},
        {"label":"negative","content":"Great, excellent, wonderful, best product."},
        {"label":"positive","content":"TRIGGER_WORD backdoor here TRIGGER_WORD"},
    ]
    assert impl.solve(samples) == [2, 3, 4]

def test_no_mismatch_equal_counts():
    samples = [{"label":"positive","content":"good bad great terrible"}]
    assert impl.solve(samples) == []

def test_neutral_content_positive_label():
    samples = [{"label":"positive","content":"The item arrived in a box."}]
    assert impl.solve(samples) == []
