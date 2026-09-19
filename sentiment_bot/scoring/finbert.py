"""FinBERT scoring with lexical fallback. CPU-safe, batched, never crashes."""
from __future__ import annotations
import re

POS_WORDS = {"beat", "beats", "record", "profit", "profits", "growth", "surge", "surges",
             "upgrade", "upgraded", "bullish", "gain", "gains", "strong", "raise", "raises",
             "outperform", "win", "wins", "approval", "deal", "partnership", "dividend"}
NEG_WORDS = {"miss", "misses", "loss", "losses", "fall", "falls", "drop", "drops", "downgrade",
             "downgraded", "bearish", "weak", "cut", "cuts", "lawsuit", "fraud", "recall",
             "layoff", "layoffs", "probe", "warning", "bankruptcy", "fine", "delay"}
LABELS = ["positive", "negative", "neutral"]

_model = None
_tokenizer = None
_device = None


def lexical_scores(texts):
    out = []
    for t in texts:
        toks = set(re.findall(r"[a-z]+", (t or "").lower()))
        p = len(toks & POS_WORDS)
        n = len(toks & NEG_WORDS)
        if p > n:
            out.append(("positive", 0.6, 0.2, 0.2, 0.4, "lexical"))
        elif n > p:
            out.append(("negative", 0.2, 0.2, 0.6, -0.4, "lexical"))
        else:
            out.append(("neutral", 0.2, 0.6, 0.2, 0.0, "lexical"))
    return out


def _load(model_name):
    global _model, _tokenizer, _device
    if _model is not None:
        return True
    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        _device = "cuda" if torch.cuda.is_available() else "cpu"
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = AutoModelForSequenceClassification.from_pretrained(model_name)
        _model.to(_device)
        _model.eval()
        return True
    except Exception as e:
        print("FinBERT load failed (%s); using lexical fallback." % e)
        _model = False
        return False


def _finbert_batch(texts, model_name):
    import torch
    enc = _tokenizer(list(texts), padding=True, truncation=True,
                     max_length=512, return_tensors="pt")
    enc = {k: v.to(_device) for k, v in enc.items()}
    with torch.no_grad():
        logits = _model(**enc).logits
        probs = torch.softmax(logits, dim=-1).cpu().tolist()
    id2label = {v.lower(): k for k, v in _model.config.id2label.items()}
    out = []
    for pr in probs:
        pos = float(pr[id2label.get("positive", 0)])
        neg = float(pr[id2label.get("negative", 1)])
        neu = float(pr[id2label.get("neutral", 2)])
        label = LABELS[[pos, neg, neu].index(max(pos, neg, neu))]
        if label == "positive":
            label = "positive"
        score = pos - neg
        out.append((label, pos, neu, neg, score, "finbert"))
    return out


def score_texts(texts, model_name="ProsusAI/finbert", batch_size=32, use_model=True):
    """Returns list of (label, pos, neu, neg, score, model_tag)."""
    texts = [(t or "")[:2000] for t in texts]
    if not use_model or not _load(model_name):
        return lexical_scores(texts)
    out = []
    for i in range(0, len(texts), batch_size):
        chunk = texts[i:i + batch_size]
        try:
            out.extend(_finbert_batch(chunk, model_name))
        except Exception as e:
            print("batch failed (%s); lexical fallback for %d items" % (e, len(chunk)))
            out.extend(lexical_scores(chunk))
    return out
